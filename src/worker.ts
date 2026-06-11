// Minimal asset server with SPA fallback under /docs/
import { Hono } from 'hono'

type Env = { Bindings: { ASSETS: Fetcher } }
const app = new Hono<Env>()

app.get('/docs', (c) => c.redirect('/docs/', 301))

// assets.directory: "build/docs"
app.get('/docs/*', async (c) => {
  const url = new URL(c.req.url)

  const stripped = new URL(url.toString())
  stripped.pathname = stripped.pathname.replace(/^\/docs(\/|$)/, '/')

  let res = await c.env.ASSETS.fetch(new Request(stripped.toString(), c.req.raw))
  res = restoreDocsBasePathRedirect(res, url.origin)

  if (res.status === 404 && (c.req.header('Accept') || '').includes('text/html')) {
    const idx = new URL('/index.html', stripped)
    const r = await c.env.ASSETS.fetch(new Request(idx.toString(), c.req.raw))
    res = new Response(r.body, r)
    res.headers.set('Content-Type', 'text/html; charset=utf-8')
  }

  return res
})

function restoreDocsBasePathRedirect(response: Response, origin: string): Response {
  if (![301, 302, 303, 307, 308].includes(response.status)) {
    return response
  }

  const location = response.headers.get('Location')
  if (!location) {
    return response
  }

  let nextLocation = location

  if (location.startsWith('/') && location !== '/docs' && !location.startsWith('/docs/')) {
    nextLocation = `/docs${location}`
  } else {
    try {
      const targetUrl = new URL(location)
      if (targetUrl.origin === origin) {
        if (!targetUrl.pathname.startsWith('/docs/')) {
          targetUrl.pathname = `/docs${targetUrl.pathname}`
        }
        nextLocation = `${targetUrl.pathname}${targetUrl.search}${targetUrl.hash}`
      }
    } catch {
      return response
    }
  }

  if (nextLocation === location) {
    return response
  }

  const rewritten = new Response(response.body, response)
  rewritten.headers.set('Location', nextLocation)
  return rewritten
}

export default app
