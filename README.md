<p>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/header-dark.svg">
  <img alt="Terminal running neofetch: Ervin Nyisztor, full-stack developer in Hungary. Stack: TypeScript, React Native, Supabase. Building JogsiGo, CleanValet and GymHero." src="./assets/header-light.svg" width="100%">
</picture>
</p>

<p>
  <a href="https://ervin-nyisztor-portfolio.vercel.app"><img alt="Portfolio" src="https://img.shields.io/badge/portfolio-visit-e9a23b?style=flat-square&labelColor=30363d"></a>
  <a href="mailto:ervinkaroly.nyisztor@gmail.com"><img alt="Email" src="https://img.shields.io/badge/email-say%20hi-e9a23b?style=flat-square&labelColor=30363d"></a>
  <img alt="Open to freelance work" src="https://img.shields.io/badge/freelance-open-3fb950?style=flat-square&labelColor=30363d">
</p>

I build mobile and web products end to end: the database, the auth, the payments, and the screens on top of them. Most of my work lives in private repos, so here is what it is.

## Currently building

<a href="https://jogsigo.expo.app"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/jogsigo-dark.svg"><img alt="JogsiGo: driving-school platform for Hungary. Expo, Supabase, Stripe Connect, Postgres RLS." src="./assets/jogsigo-light.svg" width="49%"></picture></a>
<a href="https://ervin-nyisztor-portfolio.vercel.app"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/cleanvalet-dark.svg"><img alt="CleanValet: home-cleaning marketplace with homeowner, cleaner and admin apps. React Native, Supabase, Stripe, Twilio, Sentry." src="./assets/cleanvalet-light.svg" width="49%"></picture></a>
<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/gymhero-dark.svg"><img alt="GymHero: workouts become stats that decide your hero. Expo, TypeScript, Zustand, HealthKit." src="./assets/gymhero-light.svg" width="49%"></picture>
<a href="https://ervin-nyisztor-portfolio.vercel.app"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/portfolio-dark.svg"><img alt="Portfolio: static Next.js site for dev work and music. Next.js, Tailwind, TypeScript, Vercel." src="./assets/portfolio-light.svg" width="49%"></picture></a>

## Stack

<p>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=ts%2Creact%2Cnextjs%2Ctailwind%2Cnodejs%2Cdeno%2Csupabase%2Cpostgres%2Cpython%2Cvercel%2Cgit&theme=dark">
  <img alt="TypeScript, React / React Native, Next.js, Tailwind, Node.js, Deno, Supabase, PostgreSQL, Python, Vercel, Git" src="https://skillicons.dev/icons?i=ts,react,nextjs,tailwind,nodejs,deno,supabase,postgres,python,vercel,git&theme=light">
</picture>
</p>

**Apps** TypeScript · React Native / Expo · Next.js · Tailwind<br>
**Backend** Supabase · PostgreSQL · Edge Functions (Deno) · Stripe Connect<br>
**Before that** Python: Discord bots and tools, like [Dodmail](https://github.com/Erwin-afk/Dodmail)

## How I build

- **Security lives in the database.** Row-level security, with every write going through a security-definer function instead of trusting the client.
- **Secrets never ship in the app.** Payment keys stay server-side in Edge Functions; each customer's own invoicing key is encrypted in Supabase Vault.
- **Tests run anywhere.** Database tests on PGlite, so no Docker needed, and Edge Function tests on Deno.
- **Typed end to end.** TypeScript from the screens down to the Edge Functions, with database types generated from the schema.

## Off the keyboard

I produce music as **Fenzi**: [Spotify](https://open.spotify.com/artist/13ZWncwtfgIAqEkS2cvF8z) · [YouTube](https://www.youtube.com/@prodfenzi)
