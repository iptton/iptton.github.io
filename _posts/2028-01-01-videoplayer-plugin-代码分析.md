---
title: "VideoPlayer plugin 代码分析"
date: "2018-12-14"
---

VideoPlayer 共有三个文件

- video\_player.dart （657行）
- VideoPlayerPlugin.java （386行）
- QueuingEventSink.java （82行）

还好，不算太长，先从最短的开始吧：

QueuingEventSink.java

```
/**
 * And implementation of {@link EventChannel.EventSink} which can wrap an underlying sink.
 *
 * <p>It delivers messages immediately when downstream is available, but it queues messages before
 * the delegate event sink is set with setDelegate.
 *
 * <p>This class is not thread-safe. All calls must be done on the same thread or synchronized
 * externally.
 */
```

EventChannel.EventSink 的一个实现，用于封装底层通道。此类无法保证线程安全。

```
@Override
  public void success(Object event) {
    enqueue(event);
    maybeFlush();
  }
```

此类做的事只有两件，当success 传递event 时，入列，并调用 flush ,而 flush 则是向 delegate 调用 success 方法。为什么要做一个这样的代理层？继续看看下一个 java文件：

VideoPlayerPlugin.java

此文件包含一个插件必须的类 VideoPlayerPlugin 及一个内部类 VideoPlayer。

入口函数：

```
public static void registerWith(Registrar registrar) {
    final VideoPlayerPlugin plugin = new VideoPlayerPlugin(registrar);
    final MethodChannel channel =
        new MethodChannel(registrar.messenger(), "flutter.io/videoPlayer");
    channel.setMethodCallHandler(plugin);
    registrar.addViewDestroyListener(
        new PluginRegistry.ViewDestroyListener() {
          @Override
          public boolean onViewDestroy(FlutterNativeView view) {
            plugin.onDestroy();
            return false; // We are not interested in assuming ownership of the NativeView.
          }
        });
  }
```

实例化一个 Plugin 并设置 methodChannel 及监听videDestroy事件（用于视频的销毁？）

```
  private VideoPlayerPlugin(Registrar registrar) {
    this.registrar = registrar;
    this.videoPlayers = new HashMap<>();
  }
```

plugin 的构造函数，videoPlayers 表明这个插件需考虑多个player并存的情况。

```
  @Override
  public void onMethodCall(MethodCall call, Result result) {
    TextureRegistry textures = registrar.textures();
    if (textures == null) {
      result.error("no_activity", "video_player plugin requires a foreground activity", null);
      return;
    }
    switch (call.method) {
      case "init":
        for (VideoPlayer player : videoPlayers.values()) {
          player.dispose();
        }
        videoPlayers.clear();
        break;
      case "create":
        {
          TextureRegistry.SurfaceTextureEntry handle = textures.createSurfaceTexture();
          EventChannel eventChannel =
              new EventChannel(
                  registrar.messenger(), "flutter.io/videoPlayer/videoEvents" + handle.id());

          VideoPlayer player;
          if (call.argument("asset") != null) {
            String assetLookupKey;
            if (call.argument("package") != null) {
              assetLookupKey =
                  registrar.lookupKeyForAsset(
                      (String) call.argument("asset"), (String) call.argument("package"));
            } else {
              assetLookupKey = registrar.lookupKeyForAsset((String) call.argument("asset"));
            }
            player =
                new VideoPlayer(
                    registrar.context(),
                    eventChannel,
                    handle,
                    "asset:///" + assetLookupKey,
                    result);
            videoPlayers.put(handle.id(), player);
          } else {
            player =
                new VideoPlayer(
                    registrar.context(),
                    eventChannel,
                    handle,
                    (String) call.argument("uri"),
                    result);
            videoPlayers.put(handle.id(), player);
          }
          break;
        }
      default:
        {
          long textureId = ((Number) call.argument("textureId")).longValue();
          VideoPlayer player = videoPlayers.get(textureId);
          if (player == null) {
            result.error(
                "Unknown textureId",
                "No video player associated with texture id " + textureId,
                null);
            return;
          }
          onMethodCall(call, result, textureId, player);
          break;
        }
    }
  }
```

onMethodCall ，dart 端的入口。主要逻辑有三个：

- init : 清除所有player
- create : 根据 id 创建 Texture 及 EventChannel, VideoPlayer 等
- defalut : 调用另一个 onMethodCall
    
    // "另一个 onMethodCall " private void onMethodCall(MethodCall call, Result result, long textureId, VideoPlayer player) { switch (call.method) { case "setLooping": player.setLooping((Boolean) call.argument("looping")); result.success(null); break; case "setVolume": player.setVolume((Double) call.argument("volume")); result.success(null); break; case "play": player.play(); result.success(null); break; case "pause": player.pause(); result.success(null); break; case "seekTo": int location = ((Number) call.argument("location")).intValue(); player.seekTo(location); result.success(null); break; case "position": result.success(player.getPosition()); break; case "dispose": player.dispose(); videoPlayers.remove(textureId); result.success(null); break; default: result.notImplemented(); break; }
    

这个 onMethodCall 主要把视频创建以外的生命周期函数放在一起。

以上代码都只是一个设置，核心代码要登场了：内部类 VideoPlayer

```
    private SimpleExoPlayer exoPlayer; 
    private Surface surface;
    private final TextureRegistry.SurfaceTextureEntry textureEntry;
    private QueuingEventSink eventSink = new QueuingEventSink();
    private final EventChannel eventChannel;
    private boolean isInitialized = false;
```

ExoPlayer 是 google 官方提供的一个Android视频播放器，功能比原生的 MediaPlayer API 要丰富，易于扩展及自定义。

```
    VideoPlayer(
        Context context,
        EventChannel eventChannel,
        TextureRegistry.SurfaceTextureEntry textureEntry,
        String dataSource,
        Result result) {
      // 设置 ExoPlayer
      setupVideoPlayer(eventChannel, textureEntry, result);
    }

    private void setupVideoPlayer(
        EventChannel eventChannel,
        TextureRegistry.SurfaceTextureEntry textureEntry,
        Result result) {

      eventChannel.setStreamHandler(
          new EventChannel.StreamHandler() {
            @Override
            public void onListen(Object o, EventChannel.EventSink sink) {
              eventSink.setDelegate(sink);
            }

            @Override
            public void onCancel(Object o) {
              eventSink.setDelegate(null); // setDelegate 为 null 可以避免内存泄露？
            }
          });

      surface = new Surface(textureEntry.surfaceTexture());
      exoPlayer.setVideoSurface(surface);
      setAudioAttributes(exoPlayer);

      exoPlayer.addListener(
          new DefaultEventListener() {

            @Override
            public void onPlayerStateChanged(final boolean playWhenReady, final int playbackState) {
              super.onPlayerStateChanged(playWhenReady, playbackState);
              if (playbackState == Player.STATE_BUFFERING) {
                Map<String, Object> event = new HashMap<>();
                event.put("event", "bufferingUpdate");
                List<Integer> range = Arrays.asList(0, exoPlayer.getBufferedPercentage());
                // iOS supports a list of buffered ranges, so here is a list with a single range.
                event.put("values", Collections.singletonList(range));
                eventSink.success(event);
              } else if (playbackState == Player.STATE_READY && !isInitialized) {
                isInitialized = true;
                sendInitialized();
              }
            }

            @Override
            public void onPlayerError(final ExoPlaybackException error) {
              super.onPlayerError(error);
              if (eventSink != null) {
                eventSink.error("VideoError", "Video player had error " + error, null);
              }
            }
          });

      Map<String, Object> reply = new HashMap<>();
      reply.put("textureId", textureEntry.id());
      result.success(reply);
    }

    @SuppressWarnings("deprecation")
    private static void setAudioAttributes(SimpleExoPlayer exoPlayer) {
      if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
        exoPlayer.setAudioAttributes(
            new AudioAttributes.Builder().setContentType(C.CONTENT_TYPE_MOVIE).build());
      } else {
        exoPlayer.setAudioStreamType(AudioManager.STREAM_MUSIC);
      }
    }

    void play() {
      exoPlayer.setPlayWhenReady(true);
    }

    void pause() {
      exoPlayer.setPlayWhenReady(false);
    }

    void setLooping(boolean value) {
      exoPlayer.setRepeatMode(value ? REPEAT_MODE_ALL : REPEAT_MODE_OFF);
    }

    void setVolume(double value) {
      float bracketedValue = (float) Math.max(0.0, Math.min(1.0, value));
      exoPlayer.setVolume(bracketedValue);
    }

    void seekTo(int location) {
      exoPlayer.seekTo(location);
    }

    long getPosition() {
      return exoPlayer.getCurrentPosition();
    }

    private void sendInitialized() {
      if (isInitialized) {
        Map<String, Object> event = new HashMap<>();
        event.put("event", "initialized");
        event.put("duration", exoPlayer.getDuration());
        if (exoPlayer.getVideoFormat() != null) {
          event.put("width", exoPlayer.getVideoFormat().width);
          event.put("height", exoPlayer.getVideoFormat().height);
        }
        eventSink.success(event);
      }
    }

    void dispose() {
      if (isInitialized) {
        exoPlayer.stop();
      }
      textureEntry.release();
      eventChannel.setStreamHandler(null);
      if (surface != null) {
        surface.release();
      }
      if (exoPlayer != null) {
        exoPlayer.release();
      }
    }
  }
```

以上代码可以看到，从播放到停止，flutter 和 native 之间只是传递了简单的指令，并不存在视频数据的传输 万万没想到——flutter这样外接纹理 ！
