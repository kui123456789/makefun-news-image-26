# The World Today — Thursday 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/kui123456789/makefun-news-image-26/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/kui123456789/makefun-news-image-26/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A newspaper-style front page summing up the world news of Thursday,
26 November 2026 in a single 1024×1024 image. The program draws the
page from scratch with PIL — masthead, date line, and six story panels,
each with a small hand-drawn illustration, a headline and a short summary.

## The six stories

1. **Tankers ablaze in the Strait of Hormuz** — Two oil tankers hit naval
   mines and caught fire in the strait, Iran's Revolutionary Guard said.
   (Just Security, 25 Nov)
2. **Houthis strike Saudi Arabia's biggest refinery** — Yemen's Houthis
   said they struck the Ras Tanura oil refinery; fires were reported.
   (Just Security, 25 Nov)
3. **First Pakistani astronaut reaches Tiangong** — Shenzhou-24 docked
   with China's Tiangong station, carrying Pakistan's first astronaut
   to orbit. (Xinhua, 25 Nov)
4. **Australia and Solomons sign security pact** — Canberra and Honiara
   signed a treaty barring foreign military bases in the Solomon Islands.
   (Just Security, 25 Nov)
5. **Cairo tanker fire kills at least 31** — A fuel tanker overturned on
   Cairo's Ring Road; the fire killed at least 31 people.
   (Associated Press, 25 Nov)
6. **All hostages freed in Cartagena siege** — Troops stormed a Cartagena
   supermarket and freed all hostages after a day-long siege.
   (Associated Press, 25 Nov)

All six stories happened or were first reported on 25–26 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024×1024 PNG, under 1 MiB). The program
uses only the standard library and Pillow, needs no network, and is
deterministic — two runs produce byte-identical output.
