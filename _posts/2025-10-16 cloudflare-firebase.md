


## Cloudflare

- itty-router-openapi 

`itty-router-openapi` is a library designed to simplify the creation of OpenAPI-compliant APIs, particularly for Cloudflare Workers. It functions as an extension of `itty-router`, a lightweight routing system commonly used in serverless environments.

用来快速生成调试 api

```javascript

//index.js
import { GetSearch } from './search.js';
import ittyOpenAPI from './vendor/@cloudflare/itty-router-openapi@0.1.3.js';

export const router = ittyOpenAPI.OpenAPIRouter({
  schema: {
    info: {
      title: 'GitHub Repositories Search API',
      description:
        'A plugin that allows the user to search for GitHub repositories using ChatGPT',
      version: 'v0.0.1'
    }
  },
  docs_url: '/',
  aiPlugin: {
    name_for_human: 'GitHub Repositories Search',
    name_for_model: 'github_repositories_search',
    description_for_human: 'GitHub Repositories Search plugin for ChatGPT.',
    description_for_model:
      'GitHub Repositories Search plugin for ChatGPT. You can search for GitHub repositories using this plugin.',
    contact_email: 'support@example.com',
    legal_info_url: 'http://www.example.com/legal',
    logo_url: 'https://workers.cloudflare.com/resources/logo/logo.svg'
  }
});

router.get('/search', GetSearch);

// 404 for everything else
router.all('*', () => new Response('Not Found.', { status: 404 }));

export default {
  fetch: router.handle
};



// search.js

import ittyOpenAPI from './vendor/@cloudflare/itty-router-openapi@0.1.3.js';

export class GetSearch extends ittyOpenAPI.OpenAPIRoute {
  static schema = {
    tags: ['Search'],
    summary: 'Search repositories by a query parameter',
    parameters: {
      q: ittyOpenAPI.Query(String, {
        description: 'The query to search for',
        default: 'cloudflare workers'
      })
    },
    responses: {
      200: {
        schema: {
          repos: [
            {
              name: 'itty-router-openapi',
              description:
                'OpenAPI 3 schema generator and validator for Cloudflare Workers',
              stars: '80',
              url: 'https://github.com/cloudflare/itty-router-openapi'
            }
          ]
        }
      }
    }
  };

  async handle(request, env, ctx, data) {
    const url = 'https://api.github.com/search/repositories?q=' + data.q;

    const resp = await fetch(url, {
      headers: {
        Accept: 'application/vnd.github.v3+json',
        'User-Agent': 'RepoAI - Cloudflare Workers ChatGPT Plugin Example'
      }
    });

    if (!resp.ok) {
      return new Response(await resp.text(), { status: 400 });
    }

    const json = await resp.json();

    const repos = json.items.map(item => ({
      name: item.name,
      description: item.description,
      stars: item.stargazers_count,
      url: item.html_url
    }));

    return {
      repos: repos
    };
  }
}
```

效果：根目录为设计页面

![[Pasted image 20251016234038.png]]

Cloudflare 上还有以下服务：
- workflow
- KV ，DB, R2 对象存在(文件存在)


## Firebase

