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

  if (res.status === 404 && (c.req.header('Accept') || '').includes('text/html')) {
    const idx = new URL('/index.html', stripped)
    const r = await c.env.ASSETS.fetch(new Request(idx.toString(), c.req.raw))
    res = new Response(r.body, r)
    res.headers.set('Content-Type', 'text/html; charset=utf-8')
  }

  return res
})

export default app
