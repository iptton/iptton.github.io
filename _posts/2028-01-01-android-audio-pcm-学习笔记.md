---
title: "Android Audio & PCM 学习笔记"
date: "2018-11-16"
---

[Record,play and visualize raw audio data in Android](https://www.newventuresoftware.com/blog/record-play-and-visualize-raw-audio-data-in-android)

通过 [AudioRecord](http://developer.android.com/reference/android/media/AudioRecord.html) 和 [AudioTrack](http://developer.android.com/reference/android/media/AudioTrack.html) 处理音频裸(raw)数据。

### 一些必要的理论

音频数据是**模拟信号**，转换模拟信号为**数字数据**的过程称之为**抽样(sampling)**

![](images/300px-signal_sampling.png)

> [Wikipedia](https://en.wikipedia.org/wiki/Sampling_%28signal_processing%29) : In [signal processing](https://en.wikipedia.org/wiki/Signal_processing), **sampling** is the reduction of a [continuous signal](https://en.wikipedia.org/wiki/Continuous_signal) to a [discrete signal](https://en.wikipedia.org/wiki/Discrete_signal). A common example is the conversion of a [sound wave](https://en.wikipedia.org/wiki/Sound_wave) (a continuous signal) to a sequence of samples (a discrete-time signal). A **sample** is a value or set of values at a point in time and/or space

抽样的速度称为 **sampling rate** (不知标准译法，还是取原样好了)。通常音频录制的频率为 **44100Hz** : 即每秒从模拟信号中取44100个样本。最常见的模拟信号抽样方法为 **Pulse-code modulation (PCM)**。PCM 通常用 16位数据保存(signed short)。

由于 Android 手机的音频硬件差异，设备上的对立体声(stereo) 捕获及播放等高级功能支持程度也不一。不过，好消息是，**所有设备都支持单声道 PCM**。

* * *

### 录制裸数据

录音需要用到 AudioRecord 对象，初始化参数有：来源(source)，通道(channel config)，编码格式(encoding)及缓冲大小(buffersize)。 缓冲大小的单位为 byte , 表示一次可以获取的数据，这个参数可以使用 [getMinBufferSize()](http://developer.android.com/reference/android/media/AudioRecord.html#getMinBufferSize%28int,%20int,%20int%29) 方法来计算：

```java
int bufferSize = AudioRecord.getMinBufferSize(SAMPLE_RATE,
        AudioFormat.CHANNEL_IN_MONO,
        AudioFormat.ENCODING_PCM_16BIT);

AudioRecord record = new AudioRecord(MediaRecorder.AudioSource.DEFAULT,
        44100,
        AudioFormat.CHANNEL_IN_MONO,
        AudioFormat.ENCODING_PCM_16BIT,
        bufferSize);
```

有了 AudioRecord 对象就可以开始录音了，数据需要直接拉取，就像一个持续 IO ，因此这个操作要在一个独立的线程上完成。当完成了录音操作后，需要调用 `stop` 以释放 native 资源。

```java
final int SAMPLE_RATE = 44100; // The sampling rate
boolean mShouldContinue; // Indicates if recording / playback should stop

void recordAudio() {
    new Thread(new Runnable() {
        @Override
        public void run() {
            android.os.Process.setThreadPriority(android.os.Process.THREAD_PRIORITY_AUDIO);

            // buffer size in bytes
            int bufferSize = AudioRecord.getMinBufferSize(SAMPLE_RATE,
                    AudioFormat.CHANNEL_IN_MONO,
                    AudioFormat.ENCODING_PCM_16BIT);

            if (bufferSize == AudioRecord.ERROR || bufferSize == AudioRecord.ERROR_BAD_VALUE) {
                bufferSize = SAMPLE_RATE * 2;
            }

            short[] audioBuffer = new short[bufferSize / 2];

            AudioRecord record = new AudioRecord(MediaRecorder.AudioSource.DEFAULT,
                    SAMPLE_RATE,
                    AudioFormat.CHANNEL_IN_MONO,
                    AudioFormat.ENCODING_PCM_16BIT,
                    bufferSize);

            if (record.getState() != AudioRecord.STATE_INITIALIZED) {
                Log.e(LOG_TAG, "Audio Record can't initialize!");
                return;
            }
            record.startRecording();

            Log.v(LOG_TAG, "Start recording");

            long shortsRead = 0;
            while (mShouldContinue) {
                int numberOfShort = record.read(audioBuffer, 0, audioBuffer.length);
                shortsRead += numberOfShort;

                // Do something with the audioBuffer
            }

            record.stop();
            record.release();

            Log.v(LOG_TAG, String.format("Recording stopped. Samples read: %d", shortsRead));
        }
    }).start();
}
```

每获取一次数据，线程就会阻塞直至下一块数据填满缓冲。本例中，线程会阻塞约41毫秒。因此在 pool 循环中执行的代码，需要在41毫秒内结束，否则会错过一些数据。（`译注：是错过数据，还是数据的时序不对？`）如果你要保存数据，最好的办法是用生产消费者模式。

### 播放裸数据

AudioTracker 的构造函数和 AudioRecord 很相像。AudioTracker 有两种方式获取数据：static / stream 。前者把内容全加载进内存，播放小音频文件通常都用这种方法，而后者则通常用于大文件以提升性能。

```java
int mBufferSize = AudioTrack.getMinBufferSize(SAMPLE_RATE, AudioFormat.CHANNEL_OUT_MONO,
        AudioFormat.ENCODING_PCM_16BIT);
if (mBufferSize == AudioTrack.ERROR || mBufferSize == AudioTrack.ERROR_BAD_VALUE) {
    // For some readon we couldn't obtain a buffer size
    mBufferSize = SAMPLE_RATE * CHANNELS * 2;
}

AudioTrack mAudioTrack = new AudioTrack(
        AudioManager.STREAM_MUSIC,
        SAMPLE_RATE,
        AudioFormat.CHANNEL_OUT_MONO,
        AudioFormat.ENCODING_PCM_16BIT,
        mBufferSize,
        AudioTrack.MODE_STREAM);
```

同样，播放时，需要另起线程：

```java
ShortBuffer mSamples; // the samples to play
int mNumSamples; // number of samples to play

void playAudio() {
    new Thread(new Runnable() {
        @Override
        public void run() {
            int bufferSize = AudioTrack.getMinBufferSize(SAMPLE_RATE, AudioFormat.CHANNEL_OUT_MONO,
                    AudioFormat.ENCODING_PCM_16BIT);
            if (bufferSize == AudioTrack.ERROR || bufferSize == AudioTrack.ERROR_BAD_VALUE) {
                bufferSize = SAMPLE_RATE * 2;
            }

            AudioTrack audioTrack = new AudioTrack(
                    AudioManager.STREAM_MUSIC,
                    SAMPLE_RATE,
                    AudioFormat.CHANNEL_OUT_MONO,
                    AudioFormat.ENCODING_PCM_16BIT,
                    bufferSize,
                    AudioTrack.MODE_STREAM);

            audioTrack.play();

            Log.v(LOG_TAG, "Audio streaming started");

            short[] buffer = new short[bufferSize];
            mSamples.rewind();
            int limit = mNumSamples;
            int totalWritten = 0;
            while (mSamples.position() < limit && mShouldContinue) {
                int numSamplesLeft = limit - mSamples.position();
                int samplesToWrite;
                if (numSamplesLeft >= buffer.length) {
                    mSamples.get(buffer);
                    samplesToWrite = buffer.length;
                } else {
                    for (int i = numSamplesLeft; i < buffer.length; i++) {
                        buffer[i] = 0;
                    }
                    mSamples.get(buffer, 0, numSamplesLeft);
                    samplesToWrite = numSamplesLeft;
                }
                totalWritten += samplesToWrite;
                audioTrack.write(buffer, 0, samplesToWrite);
            }

            if (!mShouldContinue) {
                audioTrack.release();
            }

            Log.v(LOG_TAG, "Audio streaming finished. Samples written: " + totalWritten);
        }
    }).start();
}
```

[PCM-baidu百科](https://baike.baidu.com/item/PCM/1568054)

[音频 （一） AudioRecord 架构简介 - csdn](https://blog.csdn.net/pashanhu6402/article/details/79983643)
