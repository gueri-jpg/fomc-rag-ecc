# Benchmark RAG FOMC 2021–2026 — 145 questions et preuves sources

**Statut : SILVER, non gold.** Toutes les questions sont conçues pour chercher dans les **93 PDF**. Les extraits ont été confrontés aux pages PDF; leur adéquation sémantique doit encore être validée par deux annotateurs et par pooling interannuel. Les pages absentes des qrels ne sont **pas** des négatifs.

**Usage :** `queries_145.jsonl` comme requêtes; `silver_qrels_PAGES.trec` comme positifs provisoires au niveau page uniquement; `qrels_double_annotation_TEMPLATE.csv` pour annoter; `POOLING_TO_REVIEW_1740.csv` pour enrichir. Ne jamais interpréter les métriques calculées sur silver comme des métriques finales exhaustives.

## FOMC_001 · factual · test

**Question :** What target range for the federal funds rate did the FOMC maintain at its January 27, 2021 meeting?

**Origine :** 2021_V2 / Q2021_001 · **Thème :** monetary_policy

- **FOMC_001_E01** — `monetary20210127a1.pdf`, p. 1, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > The Committee decided to keep the target range for the federal funds rate at 0 to 1/4 percent and expects it will be appropriate to maintain this target range until labor market conditions have reached levels consistent with the Committee’s assessments of maximum employment and inflation has risen to 2 percent and is on track to moderately exceed 2 percent for some time.

- **FOMC_001_E02** — `fomcminutes20210127.pdf`, p. 19, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > The Committee decided to keep the target range for the federal funds rate at 0 to ¼ percent and expects it will be appropriate to maintain this target range until labor market conditions have reached levels consistent with the Committee’s assessments of maximum employment and inflation has risen to 2 percent and is on track to moderately exceed 2 percent for some time.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_002 · factual · test

**Question :** What monthly amounts of Treasury securities and agency mortgage-backed securities did the FOMC commit to purchasing in January 2021?

**Origine :** 2021_V2 / Q2021_002 · **Thème :** balance_sheet

- **FOMC_002_E01** — `monetary20210127a1.pdf`, p. 3, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > o Increase the System Open Market Account holdings of Treasury securities by $80 billion per month and of agency mortgage-backed securities (MBS) by $40 billion per month.

- **FOMC_002_E02** — `fomcminutes20210127.pdf`, p. 19, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > In addition, the Federal Reserve will continue to increase its holdings of Treasury securities by at least $80 billion per month and of agency mortgage-backed securities by at least $40 billion per month until substantial further progress has been made toward the Committee’s maximum employment and price stability goals.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_003 · explanatory · dev

**Question :** Which two factors did the FOMC identify as holding down consumer price inflation at the beginning of the pandemic-era recovery?

**Origine :** 2021_V2 / Q2021_003 · **Thème :** inflation

- **FOMC_003_E01** — `monetary20210127a1.pdf`, p. 1, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > Weaker demand and earlier declines in oil prices have been holding down consumer price inflation. Overall financial conditions remain accommodative, in part reflecting policy measures to support the economy and the flow of credit to U.S. households and businesses.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_004 · factual · dev

**Question :** As the recovery regained momentum in early 2021, how did the FOMC characterize economic activity and employment?

**Origine :** 2021_V2 / Q2021_004 · **Thème :** labor

- **FOMC_004_E01** — `monetary20210317a1.pdf`, p. 1, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > Following a moderation in the pace of the recovery, indicators of economic activity and employment have turned up recently, although the sectors most adversely affected by the pandemic remain weak.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_005 · explanatory · validation

**Question :** What supply-side disruptions were expected to lift prices temporarily during the initial reopening phase?

**Origine :** 2021_V2 / Q2021_005 · **Thème :** inflation

- **FOMC_005_E01** — `fomcminutes20210317.pdf`, p. 8, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > In addition, inflation was forecast to be temporarily boosted this year by the expected emergence of some production bottlenecks and supply constraints.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_006 · explanatory · validation

**Question :** What public-health and policy-support factors were associated with stronger employment and activity during the spring reopening?

**Origine :** 2021_V2 / Q2021_006 · **Thème :** labor

- **FOMC_006_E01** — `monetary20210428a1.pdf`, p. 1, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > Amid progress on vaccinations and strong policy support, indicators of economic activity and employment have strengthened.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_007 · multi_document · dev

**Question :** During the spring 2021 inflation pickup, how did the FOMC publicly characterize rising inflation, and what did participants expect once temporary pressures faded?

**Origine :** 2021_V2 / Q2021_007 · **Thème :** inflation

- **FOMC_007_E01** — `monetary20210428a1.pdf`, p. 1, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > Inflation has risen, largely reflecting transitory factors. Overall financial conditions remain accommodative, in part reflecting policy measures to support the economy and the flow of credit to U.S. households and businesses.

- **FOMC_007_E02** — `fomcminutes20210428.pdf`, p. 9, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > After the transitory effects of these factors fade, participants generally expected measured inflation to ease. Looking further ahead, participants expected inflation to be at levels consistent with achieving the Committee’s objectives over time.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_008 · comparative · validation

**Question :** How did the interest rate paid on reserve balances change between April and June 2021?

**Origine :** 2021_V2 / Q2021_008 · **Thème :** balance_sheet

- **FOMC_008_E01** — `monetary20210428a1.pdf`, p. 3, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > • The Board of Governors of the Federal Reserve System voted unanimously to maintain the interest rate paid on required and excess reserve balances at 0.10 percent, effective April 29, 2021.

- **FOMC_008_E02** — `monetary20210616a1.pdf`, p. 3, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > • The Board of Governors of the Federal Reserve System voted unanimously to set the interest rate paid on required and excess reserve balances at 0.15 percent, effective June 17, 2021.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_009 · comparative · dev

**Question :** How did the overnight reverse repurchase agreement offering rate change between April and June 2021?

**Origine :** 2021_V2 / Q2021_009 · **Thème :** balance_sheet

- **FOMC_009_E01** — `monetary20210428a1.pdf`, p. 3, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > o Conduct overnight reverse repurchase agreement operations at an offering rate of 0.00 percent and with a per-counterparty limit of $80 billion per day; the per-counterparty limit can be temporarily increased at the discretion of the Chair.

- **FOMC_009_E02** — `monetary20210616a1.pdf`, p. 3, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > o Conduct overnight reverse repurchase agreement operations at an offering rate of 0.05 percent and with a per-counterparty limit of $80 billion per day; the per-counterparty limit can be temporarily increased at the discretion of the Chair.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_010 · explanatory · test

**Question :** In mid-2021, what pandemic-related uncertainties remained in the FOMC economic outlook despite vaccination progress?

**Origine :** 2021_V2 / Q2021_010 · **Thème :** macroeconomy

- **FOMC_010_E01** — `monetary20210616a1.pdf`, p. 1, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > The path of the economy will depend significantly on the course of the virus. Progress on vaccinations will likely continue to reduce the effects of the public health crisis on the economy, but risks to the economic outlook remain.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_011 · explanatory · dev

**Question :** In mid-2021, which supply-and-demand mechanisms did Federal Reserve staff associate with unusually large monthly price increases?

**Origine :** 2021_V2 / Q2021_011 · **Thème :** balance_sheet

- **FOMC_011_E01** — `fomcminutes20210616.pdf`, p. 8, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > In addition, the surge in demand as the economy reopened further, combined with production bottlenecks and supply constraints, contributed to the large recent monthly price increases.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_012 · comparative · dev

**Question :** How did the FOMC change its characterization of the sectors hit hardest by the pandemic as their recovery advanced?

**Origine :** 2021_V2 / Q2021_012 · **Thème :** macroeconomy

- **FOMC_012_E01** — `monetary20210728a1.pdf`, p. 1, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > The sectors most adversely affected by the pandemic have shown improvement but have not fully recovered. Inflation has risen, largely reflecting transitory factors. Overall financial conditions remain accommodative, in part reflecting policy measures to support the economy and the flow of credit to U.S. households and businesses.

- **FOMC_012_E02** — `fomcminutes20210728.pdf`, p. 13, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > In light of these developments, members decided to remove the characterization of sectors most adversely affected by the pandemic as being in a “weak” condition and to replace it with the judgment that those sectors “have not fully recovered.” They also agreed to remove the word “significantly” when characterizing the dependence of the path of the economy on the course of the virus.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_013 · multi_document · dev

**Question :** In mid-2021, how did the FOMC describe progress toward its asset-purchase goals, and how did participants assess the employment and price-stability thresholds?

**Origine :** 2021_V2 / Q2021_013 · **Thème :** labor

- **FOMC_013_E01** — `monetary20210728a1.pdf`, p. 2, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > Since then, the economy has made progress toward these goals, and the Committee will continue to assess progress in coming meetings.

- **FOMC_013_E02** — `fomcminutes20210728.pdf`, p. 4, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > Most participants judged that the Committee’s standard of “substantial further progress” toward the maximum-employment goal had not yet been met.

- **FOMC_013_E03** — `fomcminutes20210728.pdf`, p. 5, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > Looking ahead, most participants noted that, provided that the economy were to evolve broadly as they anticipated, they judged that it could be appropriate to start reducing the pace of asset purchases this year because they saw the Committee’s “substantial further progress” criterion as satisfied with respect to the price-stability goal and as close to being satisfied with respect to the maximumemployment goal.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_014 · factual · dev

**Question :** Which two standing repo arrangements were discussed as possible funding-market backstops during the 2021 policy deliberations?

**Origine :** 2021_V2 / Q2021_014 · **Thème :** balance_sheet

- **FOMC_014_E01** — `fomcminutes20210728.pdf`, p. 3, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > Finally, the manager summarized the proposed terms for the standing repurchase agreement (repo) facility (SRF) and the Foreign and International Monetary Authorities (FIMA) Repo Facility.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_015 · factual · dev

**Question :** What condition did the FOMC identify in September 2021 for potentially reducing the pace of asset purchases soon?

**Origine :** 2021_V2 / Q2021_015 · **Thème :** balance_sheet

- **FOMC_015_E01** — `monetary20210922a1.pdf`, p. 2, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > If progress continues broadly as expected, the Committee judges that a moderation in the pace of asset purchases may soon be warranted.

- **FOMC_015_E02** — `fomcminutes20210922.pdf`, p. 9, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > All participants agreed that it would be appropriate for the current meeting’s postmeeting statement to relay the Committee’s judgment that, if progress continued broadly as expected, a moderation in the pace of asset purchases may soon be warranted.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_016 · factual · dev

**Question :** What illustrative monthly reductions in Treasury and agency MBS purchases were discussed in September 2021?

**Origine :** 2021_V2 / Q2021_016 · **Thème :** balance_sheet

- **FOMC_016_E01** — `fomcminutes20210922.pdf`, p. 9, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > The path featured monthly reductions in the pace of asset purchases, by $10 billion in the case of Treasury securities and $5 billion in the case of agency mortgage-backed securities (MBS).

- **FOMC_016_E02** — `fomcminutes20210922.pdf`, p. 9, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > No decision to proceed with a moderation of asset purchases was made at the meeting, but participants generally assessed that, provided that the economic recovery remained broadly on track, a gradual tapering process that concluded around the middle of next year would likely be appropriate.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_017 · factual · dev

**Question :** During the second half of 2021, which labor-market indicators did FOMC participants use to assess progress toward maximum employment?

**Origine :** 2021_V2 / Q2021_017 · **Thème :** labor

- **FOMC_017_E01** — `fomcminutes20210922.pdf`, p. 9, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > In doing so, participants cited the progress recorded in a number of individual series, including, among others, the employment-to-population ratio, the unemployment rate, claims for unemployment insurance, job openings, nominal wage growth, and increases in payrolls, as well as in summary measures of the labor situation.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_018 · multi_document · dev

**Question :** During the late-summer 2021 Delta wave, what did the FOMC report about vulnerable sectors, and what additional effects on growth and consumer services were discussed?

**Origine :** 2021_V2 / Q2021_018 · **Thème :** balance_sheet

- **FOMC_018_E01** — `monetary20210922a1.pdf`, p. 1, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > The sectors most adversely affected by the pandemic have improved in recent months, but the rise in COVID-19 cases has slowed their recovery.

- **FOMC_018_E02** — `fomcminutes20210922.pdf`, p. 2, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > The spread of the Delta variant of the COVID-19 virus weighed on the near-term growth outlook and median respondents to the Open Market Desk’s Survey of Primary Dealers marked down projections for gross domestic product (GDP) growth and revised up projections for inflation this year.

- **FOMC_018_E03** — `fomcminutes20210922.pdf`, p. 7, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > The spread of the Delta variant was weighing on spending for some consumer services, and low inventories and high prices due to supply constraints were restraining spending on many goods, most notably motor vehicles.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_019 · factual · dev

**Question :** What monthly reductions in net asset purchases did the FOMC announce on November 3, 2021?

**Origine :** 2021_V2 / Q2021_019 · **Thème :** balance_sheet

- **FOMC_019_E01** — `monetary20211103a1.pdf`, p. 2, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > In light of the substantial further progress the economy has made toward the Committee’s goals since last December, the Committee decided to begin reducing the monthly pace of its net asset purchases by $10 billion for Treasury securities and $5 billion for agency mortgage-backed securities.

- **FOMC_019_E02** — `fomcminutes20211103.pdf`, p. 11, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > In light of the substantial further progress the economy has made toward the Committee’s goals since last December, the Committee decided to begin reducing the monthly pace of its net asset purchases by $10 billion for Treasury securities and $5 billion for agency mortgagebacked securities.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_020 · factual · test

**Question :** Following the initial tapering announcement in late 2021, what minimum monthly Treasury and agency MBS purchases were scheduled for the following two months?

**Origine :** 2021_V2 / Q2021_020 · **Thème :** balance_sheet

- **FOMC_020_E01** — `monetary20211103a1.pdf`, p. 2, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > Beginning later this month, the Committee will increase its holdings of Treasury securities by at least $70 billion per month and of agency mortgage‑backed securities by at least $35 billion per month.

- **FOMC_020_E02** — `monetary20211103a1.pdf`, p. 2, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > Beginning in December, the Committee will increase its holdings of Treasury securities by at least $60 billion per month and of agency mortgage-backed securities by at least $30 billion per month.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_021 · explanatory · dev

**Question :** How did the FOMC explain elevated inflation during the pandemic-era reopening of the economy?

**Origine :** 2021_V2 / Q2021_021 · **Thème :** inflation

- **FOMC_021_E01** — `monetary20211103a1.pdf`, p. 1, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > Inflation is elevated, largely reflecting factors that are expected to be transitory. Supply and demand imbalances related to the pandemic and the reopening of the economy have contributed to sizable price increases in some sectors.

- **FOMC_021_E02** — `monetary20220126a1.pdf`, p. 1, année 2022, grade provisoire **2/2** — CROSS_YEAR_DIRECT_CITATION_PROVISIONAL

  > Supply and demand imbalances related to the pandemic and the reopening of the economy have continued to contribute to elevated levels of inflation.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_022 · factual · dev

**Question :** In late 2021, how did the FOMC describe the effect of the summer COVID-19 wave on the recovery of the hardest-hit sectors?

**Origine :** 2021_V2 / Q2021_022 · **Thème :** macroeconomy

- **FOMC_022_E01** — `monetary20211103a1.pdf`, p. 1, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > The sectors most adversely affected by the pandemic have improved in recent months, but the summer’s rise in COVID-19 cases has slowed their recovery.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_023 · comparative · dev

**Question :** How did the FOMC description of inflation change when it dropped its reference to “transitory” factors?

**Origine :** 2021_V2 / Q2021_023 · **Thème :** inflation

- **FOMC_023_E01** — `monetary20211103a1.pdf`, p. 1, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > Inflation is elevated, largely reflecting factors that are expected to be transitory. Supply and demand imbalances related to the pandemic and the reopening of the economy have contributed to sizable price increases in some sectors.

- **FOMC_023_E02** — `monetary20211215a1.pdf`, p. 1, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > Supply and demand imbalances related to the pandemic and the reopening of the economy have continued to contribute to elevated levels of inflation.

- **FOMC_023_E03** — `fomcminutes20211215.pdf`, p. 11, année 2021, grade provisoire **2/2** — REUSE_V2_PROVISIONAL

  > As elevated inflation had persisted for longer than they had previously anticipated, members agreed that it was appropriate to remove the reference to “transitory” factors affecting inflation in the postmeeting statement and instead note that supply and demand imbalances have continued to contribute to elevated inflation.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_024 · comparative · dev

**Question :** By how much did the monthly pace of reductions in Treasury and agency MBS purchases change between November and December 2021?

**Origine :** 2021_V2 / Q2021_024 · **Thème :** balance_sheet

- **FOMC_024_E01** — `monetary20211103a1.pdf`, p. 2, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > In light of the substantial further progress the economy has made toward the Committee’s goals since last December, the Committee decided to begin reducing the monthly pace of its net asset purchases by $10 billion for Treasury securities and $5 billion for agency mortgage-backed securities.

- **FOMC_024_E02** — `monetary20211215a1.pdf`, p. 2, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > Committee decided to reduce the monthly pace of its net asset purchases by $20 billion for Treasury securities and $10 billion for agency mortgage-backed securities.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_025 · multi_document · test

**Question :** How did FOMC discussions during the second half of 2021 evolve from tapering asset purchases toward planning eventual balance-sheet runoff?

**Origine :** 2021_V2 / Q2021_025 · **Thème :** balance_sheet

- **FOMC_025_E01** — `monetary20211103a1.pdf`, p. 2, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > In light of the substantial further progress the economy has made toward the Committee’s goals since last December, the Committee decided to begin reducing the monthly pace of its net asset purchases by $10 billion for Treasury securities and $5 billion for agency mortgage-backed securities.

- **FOMC_025_E02** — `fomcminutes20211215.pdf`, p. 4, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > Almost all participants agreed that it would likely be appropriate to initiate balance sheet runoff at some point after the first increase in the target range for the federal funds rate.

- **FOMC_025_E03** — `fomcminutes20211215.pdf`, p. 4, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > However, participants judged that the appropriate timing of balance sheet runoff would likely be closer to that of policy rate liftoff than in the Committee’s previous experience.

- **FOMC_025_E04** — `fomcminutes20211215.pdf`, p. 5, année 2021, grade provisoire **1/2** — REUSE_V2_PROVISIONAL

  > Many participants judged that the appropriate pace of balance sheet runoff would likely be faster than it was during the previous normalization episode.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_026 · factual · dev

**Question :** How were housing and consumer spending being supported in January 2021?

**Origine :** MAIN_110 / Q002 · **Thème :** finance

- **FOMC_026_E01** — `fomcminutes20210127.pdf`, p. 15, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants also observed that residential investment and home sales remained robust; low interest rates were viewed as an important factor supporting the strength in housing activity.

- **FOMC_026_E02** — `fomcminutes20210127.pdf`, p. 15, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The relative strength in consumer spending on goods was supported by fiscal programs such as federal stimulus payments and expanded unemployment benefits as well as by accommodative monetary policy.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_027 · explanatory · dev

**Question :** Why did reopening schools matter for the recovery in employment?

**Origine :** MAIN_110 / Q003 · **Thème :** labor

- **FOMC_027_E01** — `fomcminutes20210317.pdf`, p. 9, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants commented that labor force participation continued to be held down by workers’ health concerns and additional childcare responsibilities associated with virtual schooling and that the pace of recovery in the labor market would depend importantly on how rapidly those affected by these issues could rejoin the labor force.

- **FOMC_027_E02** — `fomcminutes20210922.pdf`, p. 7, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants noted that the increase in labor force participation that they had expected had not yet materialized in the wake of the reopening of schools and the expiration of the extended unemployment benefits, and that this likely reflected in part concerns about the resurgence of the virus, childcare challenges, and the uncertainties generated by ongoing disruptions to in-person schooling.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_028 · factual · test

**Question :** How much was the Fed adding to its Treasury and mortgage portfolios each month in March 2021, and what milestone would allow that to change?

**Origine :** MAIN_110 / Q004 · **Thème :** balance_sheet

- **FOMC_028_E01** — `monetary20210317a1.pdf`, p. 2, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In addition, the Federal Reserve will continue to increase its holdings of Treasury securities by at least $80 billion per month and of agency mortgage‑backed securities by at least $40 billion per month until substantial further progress has been made toward the Committee’s maximum employment and price stability goals.

- **FOMC_028_E02** — `fomcminutes20210317.pdf`, p. 12, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In addition, the Federal Reserve will continue to increase its holdings of Treasury securities by at least $80 billion per month and of agency mortgage-backed securities by at least $40 billion per month until substantial further progress has been made toward the Committee’s maximum employment and price stability goals.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_029 · explanatory · validation

**Question :** Why did some officials think the effects of input shortages on prices might last beyond 2021?

**Origine :** MAIN_110 / Q006 · **Thème :** inflation

- **FOMC_029_E01** — `fomcminutes20210428.pdf`, p. 9, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > A number of participants remarked that supply chain bottlenecks and input shortages may not be resolved quickly and, if so, these factors could put upward pressure on prices beyond this year.

- **FOMC_029_E02** — `fomcminutes20210428.pdf`, p. 9, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > They noted that in some industries, supply chain disruptions appeared to be more persistent than originally anticipated and reportedly had led to higher input costs.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_030 · explanatory · dev

**Question :** How could last year’s price drops make the current annual inflation figure look higher during the reopening?

**Origine :** MAIN_110 / Q007 · **Thème :** inflation

- **FOMC_030_E01** — `fomcminutes20210616.pdf`, p. 10, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In their discussions on inflation, participants stated that they had expected inflation to move above 2 percent in the near term, in part as the drop in prices from early in the pandemic fell out of the calculation and past increases in oil prices passed through to consumer energy prices.

- **FOMC_030_E02** — `fomcminutes20210428.pdf`, p. 9, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In their comments about inflation, participants anticipated that inflation as measured by the 12-month change of the PCE price index would move above 2 percent in the near term as very low readings from early in the pandemic fall out of the calculation.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_031 · factual · dev

**Question :** Did all lenders report easier access to small-business credit in the July 2021 discussion?

**Origine :** MAIN_110 / Q008 · **Thème :** balance_sheet

- **FOMC_031_E01** — `fomcminutes20210728.pdf`, p. 8, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Although the July SLOOS banks reported, on net, easier lending standards for C&I loans to small firms over the second quarter, industry commentary suggested that the lending standards of community banks and of other lenders not included in the SLOOS remained relatively tight.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_032 · factual · dev

**Question :** What did outcome-based guidance tie future rate and balance sheet decisions to?

**Origine :** MAIN_110 / Q010 · **Thème :** balance_sheet

- **FOMC_032_E01** — `fomcminutes20210922.pdf`, p. 9, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants also reiterated that the existing outcome-based guidance implied that the paths of the federal funds rate and the balance sheet would depend on actual progress toward reaching the Committee’s maximum-employment and inflation goals.

- **FOMC_032_E02** — `fomcminutes20210616.pdf`, p. 11, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants also reiterated that the existing outcome-based guidance implied that the paths of the federal funds rate and the balance sheet would depend on actual progress toward reaching the Committee’s maximum-employment and inflation goals.

- **FOMC_032_E03** — `fomcminutes20210428.pdf`, p. 10, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants also noted that the existing outcome-based guidance implied that the path of the federal funds rate and the balance sheet would depend on actual progress toward reaching the Committee’s maximum-employment and inflation goals.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_033 · factual · dev

**Question :** What labor-market condition did the Fed want to see before moving rates off their near-zero range in December 2021?

**Origine :** MAIN_110 / Q012 · **Thème :** labor

- **FOMC_033_E01** — `monetary20211215a1.pdf`, p. 1, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In support of these goals, the Committee decided to keep the target range for the federal funds rate at 0 to 1/4 percent.

- **FOMC_033_E02** — `monetary20211215a1.pdf`, p. 1, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > With inflation having exceeded 2 percent for some time, the Committee expects it will be appropriate to maintain this target range until labor market conditions have reached levels consistent with the Committee’s assessments of maximum employment.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_034 · explanatory · validation

**Question :** What made it hard for businesses to fill orders during the Omicron wave?

**Origine :** MAIN_110 / Q013 · **Thème :** macroeconomy

- **FOMC_034_E01** — `fomcminutes20220126.pdf`, p. 15, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants noted that supply chain bottlenecks and labor shortages had continued to limit businesses’ ability to meet strong demand, with these challenges exacerbated by the emergence and spread of the Omicron variant.

- **FOMC_034_E02** — `fomcminutes20211215.pdf`, p. 9, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants noted that supply chain bottlenecks and labor shortages continued to limit businesses’ ability to meet strong demand.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_035 · explanatory · dev

**Question :** What made a rate increase seem appropriate soon at the January 2022 meeting?

**Origine :** MAIN_110 / Q014 · **Thème :** macroeconomy

- **FOMC_035_E01** — `monetary20220126a1.pdf`, p. 1, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > With inflation well above 2 percent and a strong labor market, the Committee expects it will soon be appropriate to raise the target range for the federal funds rate.

- **FOMC_035_E02** — `fomcminutes20220126.pdf`, p. 18, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Members agreed that the postmeeting statement should be updated to reflect the Committee’s expectation that it would soon be appropriate to raise the target range for the federal funds rate in light of elevated inflation pressures and the strong labor market.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_036 · comparative · dev

**Question :** How did James Bullard’s preferred March 2022 rate move differ from the adopted target?

**Origine :** MAIN_110 / Q015 · **Thème :** macroeconomy

- **FOMC_036_E01** — `monetary20220316a1.pdf`, p. 1, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In support of these goals, the Committee decided to raise the target range for the federal funds rate to 1/4 to 1/2 percent and anticipates that ongoing increases in the target range will be appropriate.

- **FOMC_036_E02** — `monetary20220316a1.pdf`, p. 2, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Voting against this action was James Bullard, who preferred at this meeting to raise the target range for the federal funds rate by 0.5 percentage point to 1/2 to 3/4 percent.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_037 · factual · validation

**Question :** What happened to Treasury market depth and the price impact of trades around the March 2022 meeting?

**Origine :** MAIN_110 / Q016 · **Thème :** balance_sheet

- **FOMC_037_E01** — `fomcminutes20220316.pdf`, p. 3, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In the Treasury market, market depth fell and the price impact of trades increased modestly in some sectors.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_038 · factual · dev

**Question :** Which parts of private demand held up despite the first-quarter downturn discussed in May 2022?

**Origine :** MAIN_110 / Q017 · **Thème :** macroeconomy

- **FOMC_038_E01** — `monetary20220504a1.pdf`, p. 1, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Although overall economic activity edged down in the first quarter, household spending and business fixed investment remained strong.

- **FOMC_038_E02** — `fomcminutes20220504.pdf`, p. 7, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > They noted, however, that these volatile components tended to contain little signal about subsequent growth and that household spending and business fixed investment had remained strong in the first quarter.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_039 · explanatory · dev

**Question :** Why did the Fed worry about lockdowns in China when assessing the US outlook?

**Origine :** MAIN_110 / Q018 · **Thème :** macroeconomy

- **FOMC_039_E01** — `monetary20220504a1.pdf`, p. 1, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In addition, COVID-related lockdowns in China are likely to exacerbate supply chain disruptions.

- **FOMC_039_E02** — `monetary20220615a1.pdf`, p. 1, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In addition, COVID-related lockdowns in China are likely to exacerbate supply chain disruptions.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_040 · explanatory · test

**Question :** Why could households keep spending despite rising prices in June 2022?

**Origine :** MAIN_110 / Q019 · **Thème :** inflation

- **FOMC_040_E01** — `fomcminutes20220615.pdf`, p. 7, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In their discussion of the household sector, participants indicated that consumption spending had remained robust, in part reflecting strong balance sheets in the household sector and a tight labor market.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_041 · factual · test

**Question :** Which household purchases besides homes did officials expect to slow as borrowing became more expensive?

**Origine :** MAIN_110 / Q020 · **Thème :** balance_sheet

- **FOMC_041_E01** — `fomcminutes20220727.pdf`, p. 7, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants anticipated that this slowdown in housing activity would continue and also expected higher borrowing costs to lead to a slowing in other interest-sensitive household expenditures, such as purchases of durable goods.

- **FOMC_041_E02** — `fomcminutes20230503.pdf`, p. 8, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants remarked that higher interest rates would continue to restrain interest-sensitive expenditures by households, such as those on housing and durable goods.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_042 · comparative · dev

**Question :** What contrast did the July 2022 statement draw between output and the jobs market?

**Origine :** MAIN_110 / Q021 · **Thème :** labor

- **FOMC_042_E01** — `monetary20220727a1.pdf`, p. 1, année 2022, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Recent indicators of spending and production have softened.

- **FOMC_042_E02** — `monetary20220727a1.pdf`, p. 1, année 2022, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Nonetheless, job gains have been robust in recent months, and the unemployment rate has remained low.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_043 · factual · dev

**Question :** What signs of better balance in the labor market did participants identify in September 2022?

**Origine :** MAIN_110 / Q022 · **Thème :** labor

- **FOMC_043_E01** — `fomcminutes20220921.pdf`, p. 7, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants noted a number of developments consistent with the labor market moving toward better balance, including a lower rate of job turnover, a moderation in employment growth, and an increase in the labor force participation rate for prime-age workers.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_044 · factual · dev

**Question :** Which industries faced unusually severe hiring shortages in November 2022, and what happened to wages there?

**Origine :** MAIN_110 / Q023 · **Thème :** labor

- **FOMC_044_E01** — `fomcminutes20221102.pdf`, p. 7, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants remarked that employers in certain sectors, such as health care, leisure and hospitality, or construction, faced particularly acute labor shortages and that these shortages were contributing to especially strong wage pressures in those sectors.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_045 · factual · dev

**Question :** How did consumers whose budgets were stretched adapt their purchases in the December 2022 discussion?

**Origine :** MAIN_110 / Q024 · **Thème :** balance_sheet

- **FOMC_045_E01** — `fomcminutes20221214.pdf`, p. 7, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants remarked that budgets were stretched for low-to-moderate-income households and that many consumers were shifting their spending to less expensive alternatives.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_046 · explanatory · validation

**Question :** Why did the staff judge corporate debt vulnerabilities to be moderate despite historically high leverage in February 2023?

**Origine :** MAIN_110 / Q025 · **Thème :** macroeconomy

- **FOMC_046_E01** — `fomcminutes20230201.pdf`, p. 7, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The staff assessed that vulnerabilities associated with household and business leverage remained moderate, noting that although measures of business leverage were at or near a historically high level, the ability of firms to service their debt has kept pace with rising debt loads and interest rates.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_047 · factual · dev

**Question :** What risk did participants associate with inflation staying high for a long time in February 2023?

**Origine :** MAIN_110 / Q026 · **Thème :** inflation

- **FOMC_047_E01** — `fomcminutes20230201.pdf`, p. 10, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > A number of participants noted the importance of longer-term inflation expectations remaining anchored and remarked that the longer inflation remained elevated, the greater the risk of inflation expectations becoming unanchored.

- **FOMC_047_E02** — `fomcminutes20230201.pdf`, p. 11, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > A number of participants observed that a policy stance that proved to be insufficiently restrictive could halt recent progress in moderating inflationary pressures, leading inflation to remain above the Committee’s 2 percent objective for a longer period, and pose a risk of inflation expectations becoming unanchored.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_048 · explanatory · dev

**Question :** Why might a bank under funding pressure become more selective about its borrowers?

**Origine :** MAIN_110 / Q027 · **Thème :** finance

- **FOMC_048_E01** — `fomcminutes20230322.pdf`, p. 7, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants assessed that the developments so far would likely lead to some weakening of credit conditions, as some banks were likely to tighten lending standards amid rising funding costs and increased concerns about liquidity.

- **FOMC_048_E02** — `fomcminutes20230503.pdf`, p. 8, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants judged that stress in the banking sector would, in coming quarters, likely induce banks to tighten lending standards by more than they would have in response to higher interest rates alone.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_049 · explanatory · test

**Question :** How could a larger-than-expected contraction in bank credit affect hiring and prices after the banking turmoil?

**Origine :** MAIN_110 / Q028 · **Thème :** inflation

- **FOMC_049_E01** — `fomcminutes20230322.pdf`, p. 8, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > As a source of downside risk to inflation, participants noted that if banks reduce the supply of credit by more than expected, the likely restraint on economic activity and hiring could put additional downward pressure on inflation.

- **FOMC_049_E02** — `fomcminutes20230322.pdf`, p. 8, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants also noted that recent developments in the banking sector would likely result in tighter credit conditions for households and businesses and weigh on economic activity, hiring, and inflation, though the extent of these effects was highly uncertain.

- **FOMC_049_E03** — `monetary20230614a1.pdf`, p. 1, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Tighter credit conditions for households and businesses are likely to weigh on economic activity, hiring, and inflation.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_050 · explanatory · test

**Question :** Why did the May 2023 staff forecast put total inflation below core inflation?

**Origine :** MAIN_110 / Q029 · **Thème :** inflation

- **FOMC_050_E01** — `fomcminutes20230503.pdf`, p. 7, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > With expected declines in consumer energy prices and a substantial moderation in food price inflation, total inflation was projected to run below core inflation this year and next.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_051 · factual · validation

**Question :** What did officials hope to learn by leaving rates unchanged in June 2023?

**Origine :** MAIN_110 / Q030 · **Thème :** macroeconomy

- **FOMC_051_E01** — `monetary20230614a1.pdf`, p. 1, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In support of these goals, the Committee decided to maintain the target range for the federal funds rate at 5 to 5-1/4 percent.

- **FOMC_051_E02** — `monetary20230614a1.pdf`, p. 1, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Holding the target range steady at this meeting allows the Committee to assess additional information and its implications for monetary policy.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_052 · explanatory · dev

**Question :** Why did the behavior of core goods prices surprise participants even as supply chains improved?

**Origine :** MAIN_110 / Q031 · **Thème :** inflation

- **FOMC_052_E01** — `fomcminutes20230614.pdf`, p. 8, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants observed that although core goods inflation had moderated since the middle of last year, it had slowed less rapidly than expected in recent months, despite data and reports from business contacts indicating that supply chain constraints had continued to ease.

- **FOMC_052_E02** — `fomcminutes20230503.pdf`, p. 9, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants observed that although core goods inflation had moderated since the middle of last year, it had decelerated less rapidly than expected in recent months, despite reports from several business contacts of supply chain constraints continuing to ease.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_053 · factual · dev

**Question :** At what level did the July 2023 increase leave the federal funds target range?

**Origine :** MAIN_110 / Q032 · **Thème :** monetary_policy

- **FOMC_053_E01** — `monetary20230726a1.pdf`, p. 1, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In support of these goals, the Committee decided to raise the target range for the federal funds rate to 5-1/4 to 5-1/2 percent.

- **FOMC_053_E02** — `fomcminutes20230726.pdf`, p. 9, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In support of the Committee’s objectives to achieve maximum employment and inflation at the rate of 2 percent over the longer run, members agreed to raise the target range for the federal funds rate to 5¼ to 5½ percent.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_054 · factual · test

**Question :** What was the September 2023 assessment of the banking system, and how could credit conditions still affect activity?

**Origine :** MAIN_110 / Q033 · **Thème :** finance

- **FOMC_054_E01** — `monetary20230920a1.pdf`, p. 1, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The U.S. banking system is sound and resilient.

- **FOMC_054_E02** — `monetary20230920a1.pdf`, p. 1, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Tighter credit conditions for households and businesses are likely to weigh on economic activity, hiring, and inflation.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_055 · factual · dev

**Question :** Did faster payroll growth in September translate into a lower unemployment rate in the November 2023 review?

**Origine :** MAIN_110 / Q034 · **Thème :** labor

- **FOMC_055_E01** — `fomcminutes20231101.pdf`, p. 3, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Although total nonfarm payroll employment rose at a faster pace in September than in previous months, the unemployment rate was unchanged at 3.8 percent; the labor force participation rate and the employment-to-population ratio were also unchanged in September.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_056 · explanatory · test

**Question :** Why might further disinflation depend increasingly on demand once supply chains and labor supply had largely recovered?

**Origine :** MAIN_110 / Q035 · **Thème :** inflation

- **FOMC_056_E01** — `fomcminutes20231213.pdf`, p. 6, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants assessed that healing in supply chains and labor supply was largely complete, and therefore that continued progress in reducing inflation may need to come mainly from further softening in product and labor demand, with restrictive monetary policy continuing to play a central role.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_057 · factual · dev

**Question :** How did the December 2023 statement describe the change in economic growth since the third quarter?

**Origine :** MAIN_110 / Q036 · **Thème :** macroeconomy

- **FOMC_057_E01** — `monetary20231213a1.pdf`, p. 1, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Recent indicators suggest that growth of economic activity has slowed from its strong pace in the third quarter.

- **FOMC_057_E02** — `fomcminutes20231213.pdf`, p. 6, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In their discussion of current economic conditions, participants observed that after stronger than expected growth of real GDP in the third quarter, recent indicators suggested that growth in economic activity had slowed.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_058 · factual · validation

**Question :** How far apart were headline and core PCE inflation in the December data reviewed in January 2024?

**Origine :** MAIN_110 / Q037 · **Thème :** inflation

- **FOMC_058_E01** — `fomcminutes20240131.pdf`, p. 5, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The price index for total personal consumption expenditures (PCE) increased 2.6 percent over the 12 months ending in December, while core PCE price inflation—which excludes changes in energy prices and many consumer food prices—was 2.9 percent over the same period.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_059 · factual · dev

**Question :** What evidence did policymakers want before starting to lower rates in March 2024?

**Origine :** MAIN_110 / Q038 · **Thème :** macroeconomy

- **FOMC_059_E01** — `monetary20240320a1.pdf`, p. 1, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee does not expect it will be appropriate to reduce the target range until it has gained greater confidence that inflation is moving sustainably toward 2 percent.

- **FOMC_059_E02** — `fomcminutes20240320.pdf`, p. 9, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants noted indicators pointing to strong economic momentum and disappointing readings on inflation in recent months and commented that they did not expect it would be appropriate to reduce the target range for the federal funds rate until they had gained greater confidence that inflation was moving sustainably toward 2 percent.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_060 · factual · test

**Question :** Which vacancy and turnover measures suggested that finding workers was becoming easier in March 2024?

**Origine :** MAIN_110 / Q039 · **Thème :** labor

- **FOMC_060_E01** — `fomcminutes20240320.pdf`, p. 8, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants cited a variety of indicators that suggested some easing in labor market conditions, including declining job vacancies, a lower quits rate, and a reduced ratio of job openings to unemployed workers.

- **FOMC_060_E02** — `fomcminutes20240320.pdf`, p. 5, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The private-sector job openings rate and the quits rate were little changed in January, and both rates were far below their year-earlier levels.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_061 · factual · dev

**Question :** What change did the May 2024 statement announce for Treasury redemptions starting in June?

**Origine :** MAIN_110 / Q040 · **Thème :** balance_sheet

- **FOMC_061_E01** — `monetary20240501a1.pdf`, p. 1, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Beginning in June, the Committee will slow the pace of decline of its securities holdings by reducing the monthly redemption cap on Treasury securities from $60 billion to $25 billion.

- **FOMC_061_E02** — `fomcminutes20240501.pdf`, p. 8, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Almost all participants expressed support for the decision to begin to slow the pace of decline of the Federal Reserve’s securities holdings in June by reducing the monthly redemption cap on Treasury securities from $60 billion to $25 billion, maintaining the monthly redemption cap on agency debt and agency mortgage‑backed securities (MBS) at $35 billion, and reinvesting any principal payments in excess of the $35 billion cap into Treasury securities.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_062 · comparative · validation

**Question :** How did the Fed’s description of progress on inflation change between May and June 2024?

**Origine :** MAIN_110 / Q041 · **Thème :** inflation

- **FOMC_062_E01** — `monetary20240501a1.pdf`, p. 1, année 2024, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In recent months, there has been a lack of further progress toward the Committee’s 2 percent inflation objective.

- **FOMC_062_E02** — `monetary20240612a1.pdf`, p. 1, année 2024, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In recent months, there has been modest further progress toward the Committee’s 2 percent inflation objective.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_063 · explanatory · dev

**Question :** Why might wealthier households have been able to keep spending in June 2024?

**Origine :** MAIN_110 / Q042 · **Thème :** finance

- **FOMC_063_E01** — `fomcminutes20240612.pdf`, p. 7, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > A few participants remarked that spending by some higher-income households was likely being bolstered by increasing asset prices.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_064 · factual · dev

**Question :** What did business contacts report about firms’ ability to raise prices in July 2024?

**Origine :** MAIN_110 / Q043 · **Thème :** inflation

- **FOMC_064_E01** — `fomcminutes20240731.pdf`, p. 7, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants noted that the recent data corroborated reports from their business contacts that firms’ pricing power was waning, as consumers appeared to be more sensitive to price increases.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_065 · explanatory · dev

**Question :** What made the September 2024 labor-market data difficult to interpret?

**Origine :** MAIN_110 / Q044 · **Thème :** labor

- **FOMC_065_E01** — `fomcminutes20240918.pdf`, p. 8, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Many participants observed that the evaluation of labor market developments had been challenging, with increased immigration, revisions to reported payroll data, and possible changes in the underlying growth rate of productivity cited as complicating factors.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_066 · factual · dev

**Question :** How large was the September 2024 rate cut, and what gave the Committee confidence to make it?

**Origine :** MAIN_110 / Q045 · **Thème :** monetary_policy

- **FOMC_066_E01** — `monetary20240918a1.pdf`, p. 1, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee has gained greater confidence that inflation is moving sustainably toward 2 percent, and judges that the risks to achieving its employment and inflation goals are roughly in balance.

- **FOMC_066_E02** — `monetary20240918a1.pdf`, p. 1, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In light of the progress on inflation and the balance of risks, the Committee decided to lower the target range for the federal funds rate by 1/2 percentage point to 4-3/4 to 5 percent.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_067 · explanatory · dev

**Question :** What drove headline inflation near or below target in advanced foreign economies other than Japan in the November 2024 review?

**Origine :** MAIN_110 / Q046 · **Thème :** inflation

- **FOMC_067_E01** — `fomcminutes20241107.pdf`, p. 4, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In the advanced AFEs excluding Japan, 12-month headline inflation slowed to near or below target levels, mainly reflecting the rapid pass-through of lower energy prices earlier this year.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_068 · comparative · test

**Question :** How did the size of the November and December 2024 cuts compare with the September cut?

**Origine :** MAIN_110 / Q047 · **Thème :** macroeconomy

- **FOMC_068_E01** — `monetary20240918a1.pdf`, p. 1, année 2024, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In light of the progress on inflation and the balance of risks, the Committee decided to lower the target range for the federal funds rate by 1/2 percentage point to 4-3/4 to 5 percent.

- **FOMC_068_E02** — `monetary20241107a1.pdf`, p. 1, année 2024, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In support of its goals, the Committee decided to lower the target range for the federal funds rate by 1/4 percentage point to 4-1/2 to 4-3/4 percent.

- **FOMC_068_E03** — `monetary20241218a1.pdf`, p. 1, année 2024, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In support of its goals, the Committee decided to lower the target range for the federal funds rate by 1/4 percentage point to 4-1/4 to 4-1/2 percent.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_069 · factual · dev

**Question :** What signs of easing labor demand went beyond the number of job openings in December 2024?

**Origine :** MAIN_110 / Q048 · **Thème :** labor

- **FOMC_069_E01** — `fomcminutes20241218.pdf`, p. 9, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants cited declines in job vacancies, the quits rate, the rate at which the unemployed were obtaining jobs, and turnover as consistent with a gradual easing in labor demand.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_070 · factual · test

**Question :** What supply-side developments helped businesses expand at the start of 2025?

**Origine :** MAIN_110 / Q049 · **Thème :** macroeconomy

- **FOMC_070_E01** — `fomcminutes20250129.pdf`, p. 14, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants noted that favorable aggregate supply developments—including increases in labor supply, business investment, and productivity—continued to support a solid expansion of business activity.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_071 · explanatory · test

**Question :** Why could resolving the debt limit complicate the Fed’s plans for bank reserves?

**Origine :** MAIN_110 / Q050 · **Thème :** balance_sheet

- **FOMC_071_E01** — `fomcminutes20250129.pdf`, p. 7, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In addition, reserves might decline quickly upon resolution of the debt limit and, at the current pace of balance sheet runoff, might potentially reach levels below those viewed by the Committee as appropriate.

- **FOMC_071_E02** — `fomcminutes20250319.pdf`, p. 4, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Reserves were likely to continue to grow, except for periods around tax dates, until a resolution of the debt limit situation and then drop quickly as the TGA is rebuilt.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_072 · comparative · validation

**Question :** How did the March 2025 decision treat Treasury runoff and agency securities differently?

**Origine :** MAIN_110 / Q051 · **Thème :** balance_sheet

- **FOMC_072_E01** — `monetary20250319a1.pdf`, p. 1, année 2025, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Beginning in April, the Committee will slow the pace of decline of its securities holdings by reducing the monthly redemption cap on Treasury securities from $25 billion to $5 billion.

- **FOMC_072_E02** — `monetary20250319a1.pdf`, p. 1, année 2025, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee will maintain the monthly redemption cap on agency debt and agency mortgage-backed securities at $35 billion.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_073 · explanatory · dev

**Question :** Why did household surveys raise doubts about future consumer spending in March 2025?

**Origine :** MAIN_110 / Q052 · **Thème :** macroeconomy

- **FOMC_073_E01** — `fomcminutes20250319.pdf`, p. 11, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants commented on a number of factors that could restrain consumption, including weaker consumer sentiment and deteriorations in expected household financial situations, as indicated by a number of household surveys, and anticipation that the robust labor income growth and significant increases in asset prices over the previous several years might not continue.

- **FOMC_073_E02** — `fomcminutes20250319.pdf`, p. 9, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Information from participants’ business contacts and from many surveys indicated some deterioration in household and business sentiment amid heightened uncertainty about government policies.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_074 · explanatory · dev

**Question :** How could import duties encourage a company to charge more even if its own goods were exempt?

**Origine :** MAIN_110 / Q053 · **Thème :** macroeconomy

- **FOMC_074_E01** — `fomcminutes20250507.pdf`, p. 10, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants noted that firms not directly subject to tariffs might take the opportunity to increase their prices if other prices rise.

- **FOMC_074_E02** — `fomcminutes20250618.pdf`, p. 9, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants noted that firms not directly subject to tariffs might take the opportunity to increase their prices if other prices rise, particularly those of complementary products.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_075 · explanatory · test

**Question :** How did swings in net exports complicate the reading of economic activity in May 2025?

**Origine :** MAIN_110 / Q054 · **Thème :** macroeconomy

- **FOMC_075_E01** — `monetary20250507a1.pdf`, p. 1, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Although swings in net exports have affected the data, recent indicators suggest that economic activity has continued to expand at a solid pace.

- **FOMC_075_E02** — `fomcminutes20250507.pdf`, p. 13, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > They noted that swings in net exports appeared to have not been fully reflected in inventory and spending data, which complicated the interpretation of the recent data on economic activity.

- **FOMC_075_E03** — `fomcminutes20250507.pdf`, p. 14, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Recognizing the measurement difficulties induced by the unusual movements in net exports in the first quarter, as businesses apparently brought in imports ahead of expected tariff increases, members agreed to acknowledge that swings in net exports had affected the data.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_076 · explanatory · dev

**Question :** What could limit the impact of tariffs on inflation according to the June 2025 minutes?

**Origine :** MAIN_110 / Q055 · **Thème :** inflation

- **FOMC_076_E01** — `fomcminutes20250618.pdf`, p. 9, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Many participants noted that the eventual effect of tariffs on inflation could be more limited if trade deals are reached soon, if firms are able to quickly adjust their supply chains, or if firms can use other margins of adjustment to reduce their exposure to the effects of tariffs.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_077 · comparative · test

**Question :** Apart from tariffs, what developments did policymakers see as risks to employment in July 2025?

**Origine :** MAIN_110 / Q056 · **Thème :** inflation

- **FOMC_077_E01** — `fomcminutes20250730.pdf`, p. 10, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In addition to tariff-induced risks, potential downside risks to employment mentioned by participants included a possible tightening of financial conditions due to a rise in risk premiums, a more substantial deterioration in the housing market, and the risk that the increased use of AI in the workplace may lower employment.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_078 · factual · validation

**Question :** How did job growth and inflation move in the September 2025 statement?

**Origine :** MAIN_110 / Q057 · **Thème :** inflation

- **FOMC_078_E01** — `monetary20250917a1.pdf`, p. 1, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Job gains have slowed, and the unemployment rate has edged up but remains low.

- **FOMC_078_E02** — `monetary20250917a1.pdf`, p. 1, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Inflation has moved up and remains somewhat elevated.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_079 · explanatory · dev

**Question :** Why were some businesses waiting before changing prices in response to trade policy?

**Origine :** MAIN_110 / Q058 · **Thème :** inflation

- **FOMC_079_E01** — `fomcminutes20251029.pdf`, p. 10, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants expressed uncertainty about the timing and magnitude of tariff-related price effects, noting that some businesses were reportedly waiting to adjust prices until tariff policies seemed more settled.

- **FOMC_079_E02** — `fomcminutes20250618.pdf`, p. 9, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Many observed that it might take some time for the effect of higher tariffs to be reflected in the prices of final goods because firms might choose not to raise prices on affected goods and services until they had run down inventories of products imported before the increase in tariffs or because it would take some time for tariffs on intermediate goods to work through the supply chain.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_080 · factual · test

**Question :** When did the October 2025 decision schedule the end of the reduction in aggregate securities holdings?

**Origine :** MAIN_110 / Q059 · **Thème :** balance_sheet

- **FOMC_080_E01** — `monetary20251029a1.pdf`, p. 1, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee decided to conclude the reduction of its aggregate securities holdings on December 1.

- **FOMC_080_E02** — `fomcminutes20251029.pdf`, p. 15, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Almost all members agreed to conclude the reduction of the Committee’s securities holdings on December 1.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_081 · explanatory · dev

**Question :** Why did the Fed plan to buy shorter-term Treasury securities in December 2025?

**Origine :** MAIN_110 / Q060 · **Thème :** balance_sheet

- **FOMC_081_E01** — `monetary20251210a1.pdf`, p. 2, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee judges that reserve balances have declined to ample levels and will initiate purchases of shorter-term Treasury securities as needed to maintain an ample supply of reserves on an ongoing basis.

- **FOMC_081_E02** — `fomcminutes20251210.pdf`, p. 4, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Accordingly, participants assessed that it was appropriate to begin RMPs and initiate purchases of shorter-term Treasury securities to maintain an ample supply of reserves over time.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_082 · factual · dev

**Question :** How did the January 2026 statement characterize hiring and unemployment?

**Origine :** MAIN_110 / Q061 · **Thème :** labor

- **FOMC_082_E01** — `monetary20260128a1.pdf`, p. 1, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Job gains have remained low, and the unemployment rate has shown some signs of stabilization.

- **FOMC_082_E02** — `fomcminutes20260128.pdf`, p. 11, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > With regard to the labor market, participants observed that the unemployment rate had held steady, on net, in recent months, while job gains had remained low.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_083 · factual · dev

**Question :** What did most longer-term inflation expectations imply about the Fed’s objective in January 2026?

**Origine :** MAIN_110 / Q062 · **Thème :** inflation

- **FOMC_083_E01** — `fomcminutes20260128.pdf`, p. 10, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants noted that most measures of longer-term inflation expectations remained consistent with the Committee’s 2 percent objective.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_084 · explanatory · validation

**Question :** Why did participants expect inflation to ease once the effects of oil prices and tariffs faded?

**Origine :** MAIN_110 / Q063 · **Thème :** inflation

- **FOMC_084_E01** — `fomcminutes20260318.pdf`, p. 8, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants anticipated that, under appropriate monetary policy, inflation would gradually move down toward the Committee’s 2 percent objective after the effect of increased tariffs and higher oil prices had faded.

- **FOMC_084_E02** — `fomcminutes20260318.pdf`, p. 7, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > With the effects of higher crude oil prices and tariffs on inflation expected to wane later this year, inflation was projected to return to its previous disinflationary trend and to be close to 2 percent by the end of next year.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_085 · factual · test

**Question :** How did the March 2026 statement characterize the US implications of developments in the Middle East?

**Origine :** MAIN_110 / Q064 · **Thème :** macroeconomy

- **FOMC_085_E01** — `monetary20260318a1.pdf`, p. 1, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The implications of developments in the Middle East for the U.S. economy are uncertain.

- **FOMC_085_E02** — `fomcminutes20260318.pdf`, p. 10, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Most participants commented that it was too early to know how developments in the Middle East would affect the U.S. economy and judged it prudent to continue to monitor the situation and assess the implications for the appropriate stance of monetary policy.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_086 · factual · validation

**Question :** Which households appeared especially exposed to higher energy costs in April 2026?

**Origine :** MAIN_110 / Q065 · **Thème :** macroeconomy

- **FOMC_086_E01** — `fomcminutes20260429.pdf`, p. 10, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants commented that higher energy prices were putting strains on households, particularly lower-income households.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_087 · factual · test

**Question :** What two sources of disinflation did participants discuss in April 2026?

**Origine :** MAIN_110 / Q066 · **Thème :** inflation

- **FOMC_087_E01** — `fomcminutes20260429.pdf`, p. 9, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants anticipated that higher productivity growth would put downward pressure on inflation, and a few of those participants remarked that the ongoing deceleration in housing services prices was likely to continue to be a source of disinflationary pressure.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_088 · explanatory · dev

**Question :** How might uncertainty abroad change an employer’s decision to add or keep staff?

**Origine :** MAIN_110 / Q067 · **Thème :** macroeconomy

- **FOMC_088_E01** — `fomcminutes20260617.pdf`, p. 9, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants cited, however, the possibility that uncertainty related to geopolitical developments or the broader economic outlook could lead firms to reduce hiring or begin implementing layoffs.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_089 · comparative · dev

**Question :** At the June 2026 FOMC meeting, how did reported payroll gains compare with underlying labor-force growth?

**Origine :** MAIN_110 / Q068 · **Thème :** labor

- **FOMC_089_E01** — `fomcminutes20260617.pdf`, p. 8, année 2026, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants generally remarked that payroll employment gains had strengthened this year and appeared roughly consistent with underlying labor force growth.

- **FOMC_089_E02** — `monetary20260617a1.pdf`, p. 1, année 2026, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Job gains have kept pace with the workforce, and the unemployment rate has changed little.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_090 · explanatory · dev

**Question :** How might investment in AI affect the economy’s productive capacity over the coming years?

**Origine :** MAIN_110 / Q069 · **Thème :** macroeconomy

- **FOMC_090_E01** — `fomcminutes20260729.pdf`, p. 9, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants suggested that AI-related investments would likely increase the growth of productivity and of potential output in the coming years.

- **FOMC_090_E02** — `fomcminutes20260916.pdf`, p. 9, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants generally judged that AI-related investments would likely contribute to stronger gains in productivity and potential output in the coming years but they noted that there was substantial uncertainty over the magnitude or timing of the effects.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_091 · factual · dev

**Question :** Which part of the economy still faced unfavorable financing costs in September 2026, and why?

**Origine :** MAIN_110 / Q070 · **Thème :** macroeconomy

- **FOMC_091_E01** — `fomcminutes20260916.pdf`, p. 8, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > A few participants commented that housing was a sector in which financial conditions did not appear supportive of activity, with mortgage rates remaining at elevated levels.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_092 · explanatory · validation

**Question :** Why did the September 2026 staff projection put growth above potential through 2028?

**Origine :** MAIN_110 / Q071 · **Thème :** macroeconomy

- **FOMC_092_E01** — `fomcminutes20260916.pdf`, p. 6, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Real GDP growth was projected to pick up over the second half of this year and to outpace potential through 2028, reflecting strong business investment, solid consumer spending, and supportive financial conditions.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_093 · explanatory · test

**Question :** Why did the October 2026 statement emphasize the value of more information for the next policy decision?

**Origine :** MAIN_110 / Q072 · **Thème :** macroeconomy

- **FOMC_093_E01** — `monetary20261028a1.pdf`, p. 1, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The accumulation of more information will help the Committee determine the policy stance appropriate to ensure a timely return of inflation to the Committee’s 2 percent goal.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_094 · explanatory · validation

**Question :** Why would the Fed tolerate inflation above target after a prolonged undershoot, yet later seek to bring it back down?

**Origine :** MAIN_110 / Q074 · **Thème :** inflation

- **FOMC_094_E01** — `monetary20210728a1.pdf`, p. 1, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > With inflation having run persistently below this longer-run goal, the Committee will aim to achieve inflation moderately above 2 percent for some time so that inflation averages 2 percent over time and longer‑term inflation expectations remain well anchored at 2 percent.

- **FOMC_094_E02** — `monetary20221102a1.pdf`, p. 1, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee anticipates that ongoing increases in the target range will be appropriate in order to attain a stance of monetary policy that is sufficiently restrictive to return inflation to 2 percent over time.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_095 · factual · dev

**Question :** How did the amounts of Treasuries and mortgage securities bought each month change as the pandemic purchase program wound down?

**Origine :** MAIN_110 / Q075 · **Thème :** balance_sheet

- **FOMC_095_E01** — `monetary20211103a1.pdf`, p. 2, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Beginning in December, the Committee will increase its holdings of Treasury securities by at least $60 billion per month and of agency mortgage-backed securities by at least $30 billion per month.

- **FOMC_095_E02** — `monetary20211215a1.pdf`, p. 2, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Beginning in January, the Committee will increase its holdings of Treasury securities by at least $40 billion per month and of agency mortgage‑backed securities by at least $20 billion per month.

- **FOMC_095_E03** — `monetary20220126a1.pdf`, p. 1, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Beginning in February, the Committee will increase its holdings of Treasury securities by at least $20 billion per month and of agency mortgage‑backed securities by at least $10 billion per month.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_096 · factual · validation

**Question :** What did officials expect wider vaccination and fewer supply constraints to do for employment and prices?

**Origine :** MAIN_110 / Q076 · **Thème :** inflation

- **FOMC_096_E01** — `monetary20211215a1.pdf`, p. 1, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Progress on vaccinations and an easing of supply constraints are expected to support continued gains in economic activity and employment as well as a reduction in inflation.

- **FOMC_096_E02** — `monetary20220126a1.pdf`, p. 1, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Progress on vaccinations and an easing of supply constraints are expected to support continued gains in economic activity and employment as well as a reduction in inflation.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_097 · comparative · dev

**Question :** How did assessments of the Ukraine war’s effects on prices and activity evolve from the initial invasion to the following winter?

**Origine :** MAIN_110 / Q077 · **Thème :** inflation

- **FOMC_097_E01** — `monetary20220316a1.pdf`, p. 1, année 2022, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The implications for the U.S. economy are highly uncertain, but in the near term the invasion and related events are likely to create additional upward pressure on inflation and weigh on economic activity.

- **FOMC_097_E02** — `monetary20220921a1.pdf`, p. 1, année 2022, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The war and related events are creating additional upward pressure on inflation and are weighing on global economic activity.

- **FOMC_097_E03** — `monetary20230201a1.pdf`, p. 1, année 2023, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Russia’s war against Ukraine is causing tremendous human and economic hardship and is contributing to elevated global uncertainty.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_098 · factual · dev

**Question :** What examples show that expensive energy can affect both inflation and households’ ability to spend?

**Origine :** MAIN_110 / Q078 · **Thème :** inflation

- **FOMC_098_E01** — `fomcminutes20211103.pdf`, p. 8, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants also observed that increases in energy prices, stronger rates of nominal wage growth, and higher housing rental costs had been forces adding to inflation.

- **FOMC_098_E02** — `monetary20260429a1.pdf`, p. 1, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Inflation is elevated, in part reflecting the recent increase in global energy prices.

- **FOMC_098_E03** — `fomcminutes20260429.pdf`, p. 10, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants commented that higher energy prices were putting strains on households, particularly lower-income households.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_099 · factual · test

**Question :** How did supply bottlenecks affect both inflation and firms’ ability to meet orders during the pandemic and reopening?

**Origine :** MAIN_110 / Q079 · **Thème :** inflation

- **FOMC_099_E01** — `fomcminutes20210428.pdf`, p. 9, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > A number of participants remarked that supply chain bottlenecks and input shortages may not be resolved quickly and, if so, these factors could put upward pressure on prices beyond this year.

- **FOMC_099_E02** — `fomcminutes20220126.pdf`, p. 15, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants noted that supply chain bottlenecks and labor shortages had continued to limit businesses’ ability to meet strong demand, with these challenges exacerbated by the emergence and spread of the Omicron variant.

- **FOMC_099_E03** — `fomcminutes20240501.pdf`, p. 8, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants pointed to geopolitical events or other factors resulting in more severe supply bottlenecks or higher shipping costs, which could put upward pressure on prices and weigh on economic growth.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_100 · explanatory · test

**Question :** How could better productivity change inflation prospects when wage growth is strong?

**Origine :** MAIN_110 / Q080 · **Thème :** inflation

- **FOMC_100_E01** — `fomcminutes20221102.pdf`, p. 7, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants noted that the recent high pace of nominal wage growth, taken together with the recent low pace of productivity growth, would, if sustained, be inconsistent with achievement of the 2 percent inflation objective.

- **FOMC_100_E02** — `fomcminutes20260318.pdf`, p. 8, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants also expected higher productivity growth, associated with technological or deregulatory developments, to put downward pressure on inflation.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_101 · factual · dev

**Question :** Which changes in participation can restrict the pool of available workers during and after a public health crisis?

**Origine :** MAIN_110 / Q081 · **Thème :** labor

- **FOMC_101_E01** — `fomcminutes20210317.pdf`, p. 9, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants commented that labor force participation continued to be held down by workers’ health concerns and additional childcare responsibilities associated with virtual schooling and that the pace of recovery in the labor market would depend importantly on how rapidly those affected by these issues could rejoin the labor force.

- **FOMC_101_E02** — `fomcminutes20250917.pdf`, p. 8, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants noted low net immigration or changes in labor force participation as factors reducing labor supply.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_102 · factual · validation

**Question :** How did hiring shortages reported in 2021 and 2022 affect wages in specific sectors?

**Origine :** MAIN_110 / Q082 · **Thème :** labor

- **FOMC_102_E01** — `fomcminutes20211215.pdf`, p. 9, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Many business contacts continued to experience difficulty hiring workers across all skill levels, noting the lack of qualified candidates as well.

- **FOMC_102_E02** — `fomcminutes20221102.pdf`, p. 7, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants remarked that employers in certain sectors, such as health care, leisure and hospitality, or construction, faced particularly acute labor shortages and that these shortages were contributing to especially strong wage pressures in those sectors.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_103 · factual · validation

**Question :** How do quitting and vacancy figures help officials tell whether competition for workers is intensifying or easing?

**Origine :** MAIN_110 / Q083 · **Thème :** labor

- **FOMC_103_E01** — `fomcminutes20220504.pdf`, p. 7, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Employment growth had continued at a strong pace, the unemployment rate had fallen to a near-50-year low, quits and job openings had remained extremely elevated, and nominal wages had continued to rise rapidly.

- **FOMC_103_E02** — `fomcminutes20240320.pdf`, p. 8, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants cited a variety of indicators that suggested some easing in labor market conditions, including declining job vacancies, a lower quits rate, and a reduced ratio of job openings to unemployed workers.

- **FOMC_103_E03** — `fomcminutes20241218.pdf`, p. 9, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants cited declines in job vacancies, the quits rate, the rate at which the unemployed were obtaining jobs, and turnover as consistent with a gradual easing in labor demand.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_104 · comparative · validation

**Question :** How did household balance sheets and changes in asset prices support consumption across 2022–2025?

**Origine :** MAIN_110 / Q084 · **Thème :** inflation

- **FOMC_104_E01** — `fomcminutes20220615.pdf`, p. 7, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In their discussion of the household sector, participants indicated that consumption spending had remained robust, in part reflecting strong balance sheets in the household sector and a tight labor market.

- **FOMC_104_E02** — `fomcminutes20240612.pdf`, p. 7, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > A few participants remarked that spending by some higher-income households was likely being bolstered by increasing asset prices.

- **FOMC_104_E03** — `fomcminutes20250730.pdf`, p. 10, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants noted that economic activity would nevertheless be supported by financial conditions, including elevated household net worth, and a couple of participants highlighted stable or low credit card delinquencies.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_105 · factual · validation

**Question :** How do households’ efforts to save money affect the prices businesses can charge?

**Origine :** MAIN_110 / Q085 · **Thème :** inflation

- **FOMC_105_E01** — `fomcminutes20221214.pdf`, p. 7, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants remarked that budgets were stretched for low-to-moderate-income households and that many consumers were shifting their spending to less expensive alternatives.

- **FOMC_105_E02** — `fomcminutes20230920.pdf`, p. 6, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > A couple of participants also remarked that households were becoming increasingly price sensitive.

- **FOMC_105_E03** — `fomcminutes20241218.pdf`, p. 8, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Many participants noted that the slowing in these components of inflation corroborated reports received from their business contacts that firms were more reluctant to increase prices, as consumers appeared to be more price sensitive and were increasingly seeking discounts.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_106 · factual · validation

**Question :** What do the minutes say about the risks facing lower-income households when living costs rise or job prospects weaken?

**Origine :** MAIN_110 / Q086 · **Thème :** macroeconomy

- **FOMC_106_E01** — `fomcminutes20221214.pdf`, p. 7, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants remarked that budgets were stretched for low-to-moderate-income households and that many consumers were shifting their spending to less expensive alternatives.

- **FOMC_106_E02** — `fomcminutes20251210.pdf`, p. 11, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants commented that lower-income households were especially concerned about their employment prospects.

- **FOMC_106_E03** — `fomcminutes20260429.pdf`, p. 10, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants commented that higher energy prices were putting strains on households, particularly lower-income households.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_107 · explanatory · dev

**Question :** What evidence links borrowing costs to both strong and weak housing activity?

**Origine :** MAIN_110 / Q087 · **Thème :** finance

- **FOMC_107_E01** — `fomcminutes20210127.pdf`, p. 15, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants also observed that residential investment and home sales remained robust; low interest rates were viewed as an important factor supporting the strength in housing activity.

- **FOMC_107_E02** — `fomcminutes20220727.pdf`, p. 7, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Many participants remarked that some of the slowing, particularly in the housing sector, reflected the emerging response of aggregate demand to the tightening of financial conditions associated with the ongoing firming of monetary policy.

- **FOMC_107_E03** — `fomcminutes20260916.pdf`, p. 8, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > A few participants commented that housing was a sector in which financial conditions did not appear supportive of activity, with mortgage rates remaining at elevated levels.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_108 · factual · dev

**Question :** How did the FOMC account for past cumulative rate increases and their delayed effects when planning further tightening in 2022–2023?

**Origine :** MAIN_110 / Q088 · **Thème :** monetary_policy

- **FOMC_108_E01** — `monetary20221102a1.pdf`, p. 1, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In determining the pace of future increases in the target range, the Committee will take into account the cumulative tightening of monetary policy, the lags with which monetary policy affects economic activity and inflation, and economic and financial developments.

- **FOMC_108_E02** — `monetary20221214a1.pdf`, p. 1, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In determining the pace of future increases in the target range, the Committee will take into account the cumulative tightening of monetary policy, the lags with which monetary policy affects economic activity and inflation, and economic and financial developments.

- **FOMC_108_E03** — `monetary20230201a1.pdf`, p. 1, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In determining the extent of future increases in the target range, the Committee will take into account the cumulative tightening of monetary policy, the lags with which monetary policy affects economic activity and inflation, and economic and financial developments.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_109 · factual · dev

**Question :** Which economic, inflation, and financial indicators did the FOMC list as inputs to policy decisions in its June 2024 statement?

**Origine :** MAIN_110 / Q089 · **Thème :** inflation

- **FOMC_109_E01** — `monetary20231213a1.pdf`, p. 2, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee’s assessments will take into account a wide range of information, including readings on labor market conditions, inflation pressures and inflation expectations, and financial and international developments.

- **FOMC_109_E02** — `monetary20240612a1.pdf`, p. 2, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee’s assessments will take into account a wide range of information, including readings on labor market conditions, inflation pressures and inflation expectations, and financial and international developments.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_110 · factual · dev

**Question :** According to the March 2023 FOMC statement, under what kind of emerging risks would the Committee reconsider its policy stance?

**Origine :** MAIN_110 / Q090 · **Thème :** macroeconomy

- **FOMC_110_E01** — `monetary20220126a1.pdf`, p. 2, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee would be prepared to adjust the stance of monetary policy as appropriate if risks emerge that could impede the attainment of the Committee’s goals.

- **FOMC_110_E02** — `monetary20230322a1.pdf`, p. 2, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee would be prepared to adjust the stance of monetary policy as appropriate if risks emerge that could impede the attainment of the Committee’s goals.

- **FOMC_110_E03** — `monetary20260318a1.pdf`, p. 1, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee would be prepared to adjust the stance of monetary policy as appropriate if risks emerge that could impede the attainment of the Committee’s goals.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_111 · comparative · validation

**Question :** How did the Committee describe the balance between employment and inflation risks while moving from a pause to rate cuts?

**Origine :** MAIN_110 / Q091 · **Thème :** inflation

- **FOMC_111_E01** — `monetary20240131a1.pdf`, p. 1, année 2024, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee judges that the risks to achieving its employment and inflation goals are moving into better balance.

- **FOMC_111_E02** — `monetary20240918a1.pdf`, p. 1, année 2024, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee has gained greater confidence that inflation is moving sustainably toward 2 percent, and judges that the risks to achieving its employment and inflation goals are roughly in balance.

- **FOMC_111_E03** — `monetary20250129a1.pdf`, p. 1, année 2025, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee judges that the risks to achieving its employment and inflation goals are roughly in balance.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_112 · comparative · dev

**Question :** How did FOMC statements describe progress toward, but not yet achievement of, the 2 percent inflation objective from late 2023 to autumn 2024?

**Origine :** MAIN_110 / Q092 · **Thème :** inflation

- **FOMC_112_E01** — `monetary20231213a1.pdf`, p. 1, année 2023, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Inflation has eased over the past year but remains elevated.

- **FOMC_112_E02** — `monetary20240731a1.pdf`, p. 1, année 2024, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Inflation has eased over the past year but remains somewhat elevated.

- **FOMC_112_E03** — `monetary20240918a1.pdf`, p. 1, année 2024, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Inflation has made further progress toward the Committee’s 2 percent objective but remains somewhat elevated.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_113 · comparative · dev

**Question :** How did the Fed’s description of employment change from robust hiring and low unemployment to slower hiring and a rising jobless rate?

**Origine :** MAIN_110 / Q093 · **Thème :** labor

- **FOMC_113_E01** — `monetary20230503a1.pdf`, p. 1, année 2023, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Job gains have been robust in recent months, and the unemployment rate has remained low.

- **FOMC_113_E02** — `monetary20240918a1.pdf`, p. 1, année 2024, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Job gains have slowed, and the unemployment rate has moved up but remains low.

- **FOMC_113_E03** — `monetary20250917a1.pdf`, p. 1, année 2025, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Job gains have slowed, and the unemployment rate has edged up but remains low.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_114 · factual · validation

**Question :** Can a central bank cut its policy rate and still let securities run off its balance sheet? What evidence did the FOMC give?

**Origine :** MAIN_110 / Q094 · **Thème :** balance_sheet

- **FOMC_114_E01** — `fomcminutes20230726.pdf`, p. 8, année 2023, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > A number of participants noted that balance sheet runoff need not end when the Committee eventually begins to reduce the target range for the federal funds rate.

- **FOMC_114_E02** — `fomcminutes20240918.pdf`, p. 10, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants discussed the importance of communicating that the ongoing reduction in the Federal Reserve’s balance sheet could continue for some time even as the Committee reduced its target range for the federal funds rate.

- **FOMC_114_E03** — `monetary20241107a1.pdf`, p. 1, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In support of its goals, the Committee decided to lower the target range for the federal funds rate by 1/4 percentage point to 4-1/2 to 4-3/4 percent.

- **FOMC_114_E04** — `monetary20241107a1.pdf`, p. 1, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee will continue reducing its holdings of Treasury securities and agency debt and agency mortgage‑backed securities.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_115 · factual · validation

**Question :** How did the Treasury redemption ceiling change in the two successive decisions to slow balance sheet runoff?

**Origine :** MAIN_110 / Q095 · **Thème :** balance_sheet

- **FOMC_115_E01** — `monetary20240501a1.pdf`, p. 1, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Beginning in June, the Committee will slow the pace of decline of its securities holdings by reducing the monthly redemption cap on Treasury securities from $60 billion to $25 billion.

- **FOMC_115_E02** — `monetary20250319a1.pdf`, p. 1, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Beginning in April, the Committee will slow the pace of decline of its securities holdings by reducing the monthly redemption cap on Treasury securities from $25 billion to $5 billion.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_116 · comparative · dev

**Question :** Why might the Fed switch from allowing securities to mature to buying short-term government debt as bank reserves fall?

**Origine :** MAIN_110 / Q096 · **Thème :** balance_sheet

- **FOMC_116_E01** — `fomcminutes20250129.pdf`, p. 7, année 2025, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In addition, reserves might decline quickly upon resolution of the debt limit and, at the current pace of balance sheet runoff, might potentially reach levels below those viewed by the Committee as appropriate.

- **FOMC_116_E02** — `monetary20251029a1.pdf`, p. 1, année 2025, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee decided to conclude the reduction of its aggregate securities holdings on December 1.

- **FOMC_116_E03** — `monetary20251210a1.pdf`, p. 2, année 2025, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee judges that reserve balances have declined to ample levels and will initiate purchases of shorter-term Treasury securities as needed to maintain an ample supply of reserves on an ongoing basis.

- **FOMC_116_E04** — `monetary20260617a1.pdf`, p. 1, année 2026, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee reaffirmed its policy of maintaining ample reserves in the banking system.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_117 · comparative · dev

**Question :** What role did anchored longer-term inflation expectations play in FOMC discussions of tightening versus easing between 2022 and 2025?

**Origine :** MAIN_110 / Q097 · **Thème :** inflation

- **FOMC_117_E01** — `fomcminutes20220921.pdf`, p. 8, année 2022, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants remarked that the Committee’s affirmation of its strong commitment to its price-stability objective, together with its forceful policy actions, had likely helped keep longer-run inflation expectations anchored.

- **FOMC_117_E02** — `fomcminutes20240731.pdf`, p. 7, année 2024, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants also observed that longer-term inflation expectations had remained well anchored and viewed this anchoring as underpinning the disinflation process.

- **FOMC_117_E03** — `fomcminutes20250917.pdf`, p. 10, année 2025, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants noted that, in these circumstances, if policy were eased too much or too soon and inflation continued to be elevated, then longer-term inflation expectations could become unanchored and make restoring price stability even more challenging.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_118 · explanatory · validation

**Question :** How might conflict abroad weaken economic activity even in economies far from the fighting?

**Origine :** MAIN_110 / Q098 · **Thème :** macroeconomy

- **FOMC_118_E01** — `monetary20220316a1.pdf`, p. 1, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The implications for the U.S. economy are highly uncertain, but in the near term the invasion and related events are likely to create additional upward pressure on inflation and weigh on economic activity.

- **FOMC_118_E02** — `fomcminutes20240501.pdf`, p. 8, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants pointed to geopolitical events or other factors resulting in more severe supply bottlenecks or higher shipping costs, which could put upward pressure on prices and weigh on economic growth.

- **FOMC_118_E03** — `fomcminutes20260617.pdf`, p. 9, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants cited, however, the possibility that uncertainty related to geopolitical developments or the broader economic outlook could lead firms to reduce hiring or begin implementing layoffs.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_119 · factual · dev

**Question :** Which channels could allow a tariff shock to raise prices gradually rather than all at once?

**Origine :** MAIN_110 / Q099 · **Thème :** inflation

- **FOMC_119_E01** — `fomcminutes20251029.pdf`, p. 10, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants expressed uncertainty about the timing and magnitude of tariff-related price effects, noting that some businesses were reportedly waiting to adjust prices until tariff policies seemed more settled.

- **FOMC_119_E02** — `fomcminutes20260128.pdf`, p. 10, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some of these participants cited reports from business contacts who expected to increase prices this year in response to cost pressures, including those related to tariffs.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_120 · factual · dev

**Question :** How have technological advances been linked to both higher productivity and possible job losses?

**Origine :** MAIN_110 / Q100 · **Thème :** macroeconomy

- **FOMC_120_E01** — `fomcminutes20240501.pdf`, p. 7, année 2024, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > A few participants commented that higher productivity growth might be sustained by the incorporation of technologies such as artificial intelligence into existing business operations or by high rates of new business formation in the technology sector.

- **FOMC_120_E02** — `fomcminutes20250730.pdf`, p. 10, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In addition to tariff-induced risks, potential downside risks to employment mentioned by participants included a possible tightening of financial conditions due to a rise in risk premiums, a more substantial deterioration in the housing market, and the risk that the increased use of AI in the workplace may lower employment.

- **FOMC_120_E03** — `fomcminutes20260729.pdf`, p. 9, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Several participants suggested that AI-related investments would likely increase the growth of productivity and of potential output in the coming years.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_121 · factual · dev

**Question :** How did participants explain the possibility of moderate output growth alongside subdued hiring in late 2025?

**Origine :** MAIN_110 / Q101 · **Thème :** labor

- **FOMC_121_E01** — `fomcminutes20251029.pdf`, p. 11, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants noted the apparent divergence between subdued job growth and moderate GDP growth, with several suggesting that this pattern might persist over time as advances in AI boost productivity growth while demographic factors constrain labor supply.

- **FOMC_121_E02** — `fomcminutes20260617.pdf`, p. 8, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants generally remarked that payroll employment gains had strengthened this year and appeared roughly consistent with underlying labor force growth.

- **FOMC_121_E03** — `monetary20260916a1.pdf`, p. 1, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Productivity growth is strong, and capital investment is robust.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_122 · comparative · dev

**Question :** What different explanations do reports give for inflation driven by supply shocks during reopening and during an energy disruption?

**Origine :** MAIN_110 / Q102 · **Thème :** inflation

- **FOMC_122_E01** — `monetary20211103a1.pdf`, p. 1, année 2021, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Supply and demand imbalances related to the pandemic and the reopening of the economy have contributed to sizable price increases in some sectors.

- **FOMC_122_E02** — `monetary20220126a1.pdf`, p. 1, année 2022, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Supply and demand imbalances related to the pandemic and the reopening of the economy have continued to contribute to elevated levels of inflation.

- **FOMC_122_E03** — `monetary20260729a1.pdf`, p. 1, année 2026, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Inflation remains elevated relative to the Committee’s 2 percent goal, in part reflecting supply shocks that have driven price increases in certain sectors, including energy.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_123 · comparative · test

**Question :** How did FOMC statements describe uncertainty from mid-2025 to spring 2026 as geopolitical conditions changed?

**Origine :** MAIN_110 / Q103 · **Thème :** macroeconomy

- **FOMC_123_E01** — `monetary20250618a1.pdf`, p. 1, année 2025, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Uncertainty about the economic outlook has diminished but remains elevated.

- **FOMC_123_E02** — `monetary20250730a1.pdf`, p. 1, année 2025, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Uncertainty about the economic outlook remains elevated.

- **FOMC_123_E03** — `monetary20260318a1.pdf`, p. 1, année 2026, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The implications of developments in the Middle East for the U.S. economy are uncertain.

- **FOMC_123_E04** — `monetary20260429a1.pdf`, p. 1, année 2026, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Developments in the Middle East are contributing to a high level of uncertainty about the economic outlook.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_124 · comparative · dev

**Question :** What distinguishes a statement that leaves rates unchanged to gather information from one that announces a cut after conditions improve?

**Origine :** MAIN_110 / Q104 · **Thème :** macroeconomy

- **FOMC_124_E01** — `monetary20230614a1.pdf`, p. 1, année 2023, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Holding the target range steady at this meeting allows the Committee to assess additional information and its implications for monetary policy.

- **FOMC_124_E02** — `monetary20240918a1.pdf`, p. 1, année 2024, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee has gained greater confidence that inflation is moving sustainably toward 2 percent, and judges that the risks to achieving its employment and inflation goals are roughly in balance.

- **FOMC_124_E03** — `monetary20240918a1.pdf`, p. 1, année 2024, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In light of the progress on inflation and the balance of risks, the Committee decided to lower the target range for the federal funds rate by 1/2 percentage point to 4-3/4 to 5 percent.

- **FOMC_124_E04** — `monetary20261028a1.pdf`, p. 1, année 2026, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The accumulation of more information will help the Committee determine the policy stance appropriate to ensure a timely return of inflation to the Committee’s 2 percent goal.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_125 · comparative · dev

**Question :** How does the Fed describe the interaction between credit availability and economic growth during banking stress and after earlier rate increases?

**Origine :** MAIN_110 / Q105 · **Thème :** finance

- **FOMC_125_E01** — `monetary20231101a1.pdf`, p. 1, année 2023, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Tighter financial and credit conditions for households and businesses are likely to weigh on economic activity, hiring, and inflation.

- **FOMC_125_E02** — `fomcminutes20240320.pdf`, p. 7, année 2024, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The lagged effects of earlier monetary policy actions, through their continued contribution to tight financial and credit conditions, were still expected to hold output growth in 2024 below the staff’s estimate of potential growth.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_126 · explanatory · dev

**Question :** Why can stronger household spending coexist with shortages that push up prices?

**Origine :** MAIN_110 / Q106 · **Thème :** inflation

- **FOMC_126_E01** — `fomcminutes20210127.pdf`, p. 15, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The relative strength in consumer spending on goods was supported by fiscal programs such as federal stimulus payments and expanded unemployment benefits as well as by accommodative monetary policy.

- **FOMC_126_E02** — `fomcminutes20220126.pdf`, p. 15, année 2022, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants noted that supply chain bottlenecks and labor shortages had continued to limit businesses’ ability to meet strong demand, with these challenges exacerbated by the emergence and spread of the Omicron variant.

- **FOMC_126_E03** — `monetary20211215a1.pdf`, p. 1, année 2021, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Supply and demand imbalances related to the pandemic and the reopening of the economy have continued to contribute to elevated levels of inflation.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_127 · comparative · dev

**Question :** How did the financial pressure on households differ when credit was readily available and when banks were expected to tighten lending?

**Origine :** MAIN_110 / Q107 · **Thème :** finance

- **FOMC_127_E01** — `monetary20210728a1.pdf`, p. 1, année 2021, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Overall financial conditions remain accommodative, in part reflecting policy measures to support the economy and the flow of credit to U.S. households and businesses.

- **FOMC_127_E02** — `monetary20230322a1.pdf`, p. 1, année 2023, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Recent developments are likely to result in tighter credit conditions for households and businesses and to weigh on economic activity, hiring, and inflation.

- **FOMC_127_E03** — `monetary20231101a1.pdf`, p. 1, année 2023, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Tighter financial and credit conditions for households and businesses are likely to weigh on economic activity, hiring, and inflation.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_128 · comparative · test

**Question :** How did FOMC reports describe the effects of falling versus rising oil prices on inflation between 2021 and 2026?

**Origine :** MAIN_110 / Q108 · **Thème :** inflation

- **FOMC_128_E01** — `monetary20210127a1.pdf`, p. 1, année 2021, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Weaker demand and earlier declines in oil prices have been holding down consumer price inflation.

- **FOMC_128_E02** — `fomcminutes20210616.pdf`, p. 10, année 2021, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > In their discussions on inflation, participants stated that they had expected inflation to move above 2 percent in the near term, in part as the drop in prices from early in the pandemic fell out of the calculation and past increases in oil prices passed through to consumer energy prices.

- **FOMC_128_E03** — `fomcminutes20260318.pdf`, p. 8, année 2026, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Participants anticipated that, under appropriate monetary policy, inflation would gradually move down toward the Committee’s 2 percent objective after the effect of increased tariffs and higher oil prices had faded.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_129 · factual · dev

**Question :** Which indicators can show solid business activity when investment and productivity are supporting growth?

**Origine :** MAIN_110 / Q109 · **Thème :** macroeconomy

- **FOMC_129_E01** — `fomcminutes20250129.pdf`, p. 14, année 2025, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Some participants noted that favorable aggregate supply developments—including increases in labor supply, business investment, and productivity—continued to support a solid expansion of business activity.

- **FOMC_129_E02** — `monetary20260916a1.pdf`, p. 1, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Productivity growth is strong, and capital investment is robust.

- **FOMC_129_E03** — `monetary20261028a1.pdf`, p. 1, année 2026, grade provisoire **2/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Productivity growth is strong, and capital investment is robust.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_130 · comparative · dev

**Question :** How do the reports describe the shift from policies supporting credit during the pandemic to a restrictive stance aimed at curbing inflation?

**Origine :** MAIN_110 / Q110 · **Thème :** inflation

- **FOMC_130_E01** — `monetary20210616a1.pdf`, p. 1, année 2021, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Overall financial conditions remain accommodative, in part reflecting policy measures to support the economy and the flow of credit to U.S. households and businesses.

- **FOMC_130_E02** — `monetary20220126a1.pdf`, p. 1, année 2022, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > Overall financial conditions remain accommodative, in part reflecting policy measures to support the economy and the flow of credit to U.S. households and businesses.

- **FOMC_130_E03** — `monetary20221102a1.pdf`, p. 1, année 2022, grade provisoire **1/2** — PROVISIONAL_FACET_GRADE_NOT_GOLD

  > The Committee anticipates that ongoing increases in the target range will be appropriate in order to attain a stance of monetary policy that is sufficiently restrictive to return inflation to 2 percent over time.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_131 · factual · dev

**Question :** How did cumulative monetary tightening affect housing and business investment in the June 2023 FOMC discussion?

**Origine :** SUPP_2023_24 / Q06 · **Thème :** monetary_policy

- **FOMC_131_E01** — `fomcminutes20230614.pdf`, p. 7, année 2023, grade provisoire **2/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > In assessing the economic outlook, most participants noted that real GDP growth had been resilient in recent quarters. Participants generally judged that growth would be subdued over the remainder of this year. They assessed that the cumulative tightening of monetary policy over the past year had contributed significantly to more restrictive financial conditions and lower demand in the most interest rate sensitive sectors of the economy, especially housing and business investment. Participants also acknowledged uncertainty about the lags with which monetary policy affects the economy and discussed the extent to which the full effects of monetary tightening on the economy had been realized. While total inflation had moderated over the past year, core inflation had not shown a sustained easing since the beginning of the year. With inflation well above the Committee’s longer-run 2 percent objective, participants expected that a period of below-trend growth in real GDP and some softening in labor market conditions would be needed to bring aggregate supply and aggregate demand into better balance and reduce inflationary pressures sufficiently to return inflation to 2 percent over time.

- **FOMC_131_E02** — `fomcminutes20240612.pdf`, p. 7, année 2024, grade provisoire **0/2** — EXCLUDE_SCOPE

  > **Écarté des preuves positives :** Source is June 2024, not the June 2023 discussion asked about. Later corroboration is not a direct answer to this meeting-specific question.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_132 · explanatory · validation

**Question :** What factors did participants cite for the rise in long-term Treasury yields and mortgage rates in autumn 2023?

**Origine :** SUPP_2023_24 / Q09 · **Thème :** balance_sheet

- **FOMC_132_E01** — `fomcminutes20231101.pdf`, p. 7, année 2023, grade provisoire **2/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > Participants noted that in recent months, financial conditions had tightened significantly because of a substantial run-up in longer-term Treasury yields, among other factors. Higher Treasury yields contributed to an increase in 30-year mortgage rates to levels not seen in many years and led to higher corporate borrowing rates. Many participants observed that a range of measures suggested that the rise in longer-term yields had been driven primarily or substantially by a rise in the term premiums on Treasury securities. Participants generally viewed factors such as a fiscal outlook that suggested greater future supply of Treasury securities than previously thought and increased uncertainty about the economic and policy outlooks as likely having contributed to the rise in the term premiums. Some participants noted that the rise in longer-term yields may also have been driven by expectations for a higher path of the federal funds rate in light of the surprising resilience of the economy or a possible rise in the neutral policy rate. Participants highlighted that longer-term yields could be volatile and that the factors behind the recent increase, as well as their persistence, were uncertain. However, they also noted that, whatever the source of the rise in longer-term yields, persistent changes in financial conditions could have implications for the path of monetary policy and that it would therefore be important to continue to monitor market developments closely.

- **FOMC_132_E02** — `fomcminutes20240131.pdf`, p. 5, année 2024, grade provisoire **0/2** — EXCLUDE_SCOPE

  > **Écarté des preuves positives :** January 2024 page describes subsequently declining Treasury yields and easing rather than reasons for the autumn 2023 rise.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_133 · explanatory · validation

**Question :** Why did FOMC participants distinguish headline GDP growth from underlying private domestic demand in their 2024 discussions?

**Origine :** SUPP_2023_24 / Q10 · **Thème :** macroeconomy

- **FOMC_133_E01** — `fomcminutes20240131.pdf`, p. 7, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > Participants’ Views on Current Conditions and the Economic Outlook In their discussion of current economic conditions, participants noted that recent indicators suggested that economic activity had been expanding at a solid pace. Real GDP growth in the fourth quarter of last year came in above 3 percent at an annual rate, below the strong growth posted in the third quarter but still above most forecasters’ expectations. Participants observed that the unexpected strength in real GDP growth in the fourth quarter reflected stronger-than-expected net exports and inventory investment, which tend to be volatile and may carry little signal for future growth. Still, consumption continued to grow at a solid pace. In addition to strong

- **FOMC_133_E02** — `fomcminutes20240731.pdf`, p. 8, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > PDFP growth, which usually gives a better signal than GDP growth of economic momentum, also moderated in the first half, but by less than GDP growth. PDFP expanded at a solid pace, supported by growth in consumer spending and business fixed investment.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_134 · comparative · dev

**Question :** How did 2024 FOMC discussions contrast financial pressures on lower-income households with spending by wealthier households?

**Origine :** SUPP_2023_24 / Q11 · **Thème :** finance

- **FOMC_134_E01** — `fomcminutes20240501.pdf`, p. 7, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > In their discussion of the outlook for the household sector, participants observed that consumer spending remained firm in the first quarter, supported by low unemployment and solid income growth. A number of participants judged that consumption growth was likely to moderate this year, as growth in labor income was expected to slow and the financial positions of many households were expected to weaken. Many participants noted signs that the finances of low- and moderate-income households were increasingly coming under pressure, which these participants saw as a downside risk to the outlook for consumption. They pointed to increased usage of credit cards and buy-now-pay-later services, as well as increased delinquency rates for some types of consumer loans. In addition, elevated housing costs were adding to financial strains for lower-income households. A couple of participants noted that financial conditions appeared favorable for wealthier households, which account for a large portion of aggregate consumption, with hefty wealth gains resulting from recent equity and house price increases.

- **FOMC_134_E02** — `fomcminutes20240731.pdf`, p. 8, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > Several participants cited reports that consumers, especially those in lower-income households, were shifting away from discretionary spending and switching to lower-cost food items and brands. A couple of participants remarked that spending by some higher-income households was likely being bolstered by wealth effects from equity and housing price appreciation.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_135 · factual · dev

**Question :** How did high borrowing costs and tighter bank lending influence firms’ investment plans during 2023?

**Origine :** SUPP_2023_24 / Q13 · **Thème :** finance

- **FOMC_135_E01** — `fomcminutes20230503.pdf`, p. 8, année 2023, grade provisoire **2/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > Regarding the business sector, participants observed that growth in business fixed investment was subdued in the first quarter, reflecting relatively high borrowing costs, weak growth of business-sector output, and businesses’ increasing concerns about the general economic outlook. Participants expected the tightening of bank lending standards to weigh further on firms’ capital expenditures. Several participants noted that, based on reports from their District contacts, concerns related to banking-sector stress could add more uncertainty to an already soft economic outlook, increasing firms’ caution, especially at smaller and mid-sized firms that rely heavily on bank credit to finance their operations. However, some other participants mentioned that developments in the banking sector appeared to have had only a modest effect so far on credit availability for firms.

- **FOMC_135_E02** — `fomcminutes20231101.pdf`, p. 7, année 2023, grade provisoire **2/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > that their business contacts had reported that cost increases could not be easily passed on to customers. Several participants commented that the apparent resolution of the United Auto Workers strike would reduce business-sector uncertainty. Several participants noted that an increasing number of District businesses were reporting that higher interest rates were affecting their businesses or that firms were increasingly cutting or delaying their investment plans because of higher borrowing costs and tighter bank lending conditions. A few participants noted that the tighter financial and credit conditions could be particularly challenging for small businesses. A few participants observed that higher interest rates were also affecting the agricultural sector, with their contacts noting that high financing costs were likely weighing on purchases of heavy agricultural equipment. Regarding the energy sector, a few participants observed that energy markets had calmed after significant volatility at the start of the current armed conflict between Israel and Hamas.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_136 · factual · validation

**Question :** How did immigration and labor-force participation affect wage pressures in FOMC assessments during early 2024?

**Origine :** SUPP_2023_24 / Q14 · **Thème :** labor

- **FOMC_136_E01** — `fomcminutes20240131.pdf`, p. 8, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > ratio of job openings to unemployed workers had declined over the past year but still remained somewhat above its pre-pandemic level. Consistent with a reduction in labor market tightness, business contacts in several Districts reported an easing in wage pressures or an increased ability to hire and retain workers. Participants mentioned several developments that had boosted labor supply last year, including higher labor force participation, immigration, and an improved job-matching process; however, a few participants judged that further increases in labor supply may be limited, pointing, for instance, to the decline in labor force participation in December. While labor market conditions were generally seen as strong, several participants noted that recent job gains were concentrated in a few sectors, which, in their view, pointed to downside risks to the outlook for employment.

- **FOMC_136_E02** — `fomcminutes20240320.pdf`, p. 8, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > Participants assessed that demand and supply in the labor market were continuing to come into better balance, although conditions generally remained tight. Participants noted strong recent payroll growth, while the unemployment rate remained low. Participants cited a variety of indicators that suggested some easing in labor market conditions, including declining job vacancies, a lower quits rate, and a reduced ratio of job openings to unemployed workers. Some participants indicated that business contacts had reported less difficulty in hiring or retaining workers. Several participants noted that the better balance between labor supply and demand had contributed to an easing of nominal wage pressures. Nevertheless, some participants observed that portions of the labor market, such as the health-care sector and in less urban areas, remained very tight. Most participants noted that, during the past year, labor supply had been boosted by increased labor force participation as well as by immigration. Participants further commented that recent estimates of greater immigration in the past few years and an overall increase in labor supply could help explain the strength in employment gains even as Page 8 Federal Open Market Committee _____________________________________________________________________________________________

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_137 · factual · dev

**Question :** What did FOMC participants say about anchored longer-term inflation expectations and the disinflation outlook in 2024?

**Origine :** SUPP_2023_24 / Q15 · **Thème :** inflation

- **FOMC_137_E01** — `fomcminutes20240320.pdf`, p. 8, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > In their outlook for inflation, participants noted that they continued to expect that inflation would return to 2 percent over the medium term. They remained concerned that elevated inflation continued to harm households, especially those least able to meet the higher costs of essentials like food, housing, and transportation. A few participants remarked that they expected core nonhousing services inflation to decline as the labor market continued to move into better balance and wage growth moderated further. Participants discussed the stillelevated rate of housing services inflation and commented on the uncertainty regarding when and by how much lower readings for rent growth on new leases would pass through to this category of inflation. Several participants noted that the disinflationary pressure for core goods that had resulted from the receding of supply chain bottlenecks was likely to moderate. Other factors related to aggregate supply, such as increases in the labor force or better productivity growth, were viewed by several participants as likely to support continued disinflation. Some participants reported that business contacts had indicated that they were less able to pass on price increases or that consumers were becoming more sensitive to price changes. Some participants observed that longer-term inflation expectations appeared to remain well anchored, as reflected in a broad range of surveys of households, businesses, and forecasters, as well as measures from financial markets.

- **FOMC_137_E02** — `fomcminutes20240731.pdf`, p. 7, année 2024, grade provisoire **2/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > Participants also observed that longer-term inflation expectations had remained well anchored and viewed this anchoring as underpinning the disinflation process. A couple of participants noted that inflation pressures might persist for some time, as they assessed that the economy had considerable momentum, and that, even with some easing of the demand for labor, the labor market remained strong. Participants assessed that supply and demand conditions in the labor market had continued to come into better balance. The unemployment rate had moved up but remained low, having risen 0.7 percentage point since its trough in April 2023 to 4.1 percent in June.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_138 · comparative · dev

**Question :** How did the overnight repo and reverse repo rates and limits specified in the FOMC implementation directives change between March and September 2024?

**Origine :** SUPP_2023_24 / Q16 · **Thème :** balance_sheet

- **FOMC_138_E01** — `monetary20240320a1.pdf`, p. 3, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > o Conduct standing overnight repurchase agreement operations with a minimum bid rate of 5.5 percent and with an aggregate operation limit of $500 billion. o Conduct standing overnight reverse repurchase agreement operations at an offering rate of 5.3 percent and with a per-counterparty limit of $160 billion per day.

- **FOMC_138_E02** — `monetary20240918a1.pdf`, p. 3, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > o Conduct standing overnight repurchase agreement operations with a minimum bid rate of 5 percent and with an aggregate operation limit of $500 billion. o Conduct standing overnight reverse repurchase agreement operations at an offering rate of 4.8 percent and with a per-counterparty limit of $160 billion per day.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_139 · explanatory · test

**Question :** Why did participants in March 2024 discuss slowing balance-sheet runoff while reserve balances were still abundant?

**Origine :** SUPP_2023_24 / Q17 · **Thème :** balance_sheet

- **FOMC_139_E01** — `fomcminutes20240320.pdf`, p. 4, année 2024, grade provisoire **2/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > Considerations for Slowing the Pace of Balance Sheet Reduction Participants began a discussion related to slowing the pace of balance sheet runoff consistent with the Committee’s Plans for Reducing the Size of the Federal Reserve’s Balance Sheet announced in May 2022. Those plans indicated that in order to ensure a smooth transition, the Committee intends to slow and then stop the decline in the size of the balance sheet when reserve balances are somewhat above the level it judges to be consistent with ample reserves. Since balance sheet runoff began in June 2022, the Federal Reserve’s total securities holdings had declined roughly $1.5 trillion. In light of the ongoing sizable decline in the balance sheet, and the prospect of a more rapid decline in reserve balances, participants agreed that their discussions at this meeting would help inform the Committee’s future decisions regarding how and when to slow the pace of runoff. No decisions about adjusting the pace of balance sheet runoff were made at the meeting.

- **FOMC_139_E02** — `fomcminutes20240320.pdf`, p. 5, année 2024, grade provisoire **2/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > Participants also shared their initial perspectives on longer-term aspects of balance sheet policy beyond the more immediate issues concerning slowing the pace of runoff. Although they saw the current level of reserves as abundant, participants emphasized the underlying uncertainty about the level of reserves consistent with operating in an ample-reserves regime. They noted various price and quantity metrics that they saw as important real-time indicators of conditions in short-term funding markets that could provide signals that reserves are approaching a level somewhat above ample. Some participants also mentioned the importance of both the discount window and the standing repo facility as liquidity backstops as reserves decline. Many participants commented on aspects of the composition of the Federal Reserve’s securities holdings, including the appropriate longer-run maturity composition of the System Open Market Account portfolio and options to achieve in the longer run a portfolio that consists primarily of Treasury securities.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_140 · factual · validation

**Question :** Which foreign central banks were described as cutting policy rates during the period before the September 2024 FOMC meeting?

**Origine :** SUPP_2023_24 / Q18 · **Thème :** monetary_policy

- **FOMC_140_E01** — `fomcminutes20240918.pdf`, p. 2, année 2024, grade provisoire **2/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > In international developments, many central banks in advanced foreign economies (AFEs) had begun or continued to lower policy rates during the intermeeting period, with the Bank of England (BOE) deciding to initiate its rate-cutting cycle with a 25 basis point reduction and the European Central Bank (ECB) and the Bank of Canada (BOC) delivering their second and third 25 basis point cut, respectively.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_141 · factual · test

**Question :** What macroeconomic considerations accompanied the FOMC decisions to keep the federal funds rate at 5¼–5½ percent in September and December 2023?

**Origine :** SUPP_2023_24 / Q19 · **Thème :** monetary_policy

- **FOMC_141_E01** — `monetary20230920a1.pdf`, p. 1, année 2023, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > Recent indicators suggest that economic activity has been expanding at a solid pace. Job gains have slowed in recent months but remain strong, and the unemployment rate has remained low. Inflation remains elevated. The U.S. banking system is sound and resilient. Tighter credit conditions for households and businesses are likely to weigh on economic activity, hiring, and inflation. The extent of these effects remains uncertain. The Committee remains highly attentive to inflation risks. The Committee seeks to achieve maximum employment and inflation at the rate of 2 percent over the longer run. In support of these goals, the Committee decided to maintain the target range for the federal funds rate at 5-1/4 to 5-1/2 percent. The Committee will continue to assess additional information and its implications for monetary policy.

- **FOMC_141_E02** — `monetary20231213a1.pdf`, p. 1, année 2023, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > Recent indicators suggest that growth of economic activity has slowed from its strong pace in the third quarter. Job gains have moderated since earlier in the year but remain strong, and the unemployment rate has remained low. Inflation has eased over the past year but remains elevated. The U.S. banking system is sound and resilient. Tighter financial and credit conditions for households and businesses are likely to weigh on economic activity, hiring, and inflation. The extent of these effects remains uncertain. The Committee remains highly attentive to inflation risks. The Committee seeks to achieve maximum employment and inflation at the rate of 2 percent over the longer run. In support of these goals, the Committee decided to maintain the target range for the federal funds rate at 5-1/4 to 5-1/2 percent. The Committee will continue to assess additional information and its implications for monetary policy.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_142 · comparative · test

**Question :** How did the rationale for the first policy rate cut of September 2024 differ from the rationale discussed for the subsequent November adjustment?

**Origine :** SUPP_2023_24 / Q20 · **Thème :** monetary_policy

- **FOMC_142_E01** — `fomcminutes20240918.pdf`, p. 9, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > In light of the progress on inflation and the balance of risks, all participants agreed that it was appropriate to ease the stance of monetary policy. Given the significant progress made since the Committee first set its target range for the federal funds rate at 5¼ to 5½ percent, a substantial majority of participants supported lowering the target range for the federal funds rate by 50 basis points to 4¾ to 5 percent. These participants generally observed that such a recalibration of the stance of monetary policy would begin to bring it into better alignment with recent indicators of inflation and the labor market. They also emphasized that such a move would help sustain the strength in the economy and the labor market while continuing to promote progress on inflation, and would reflect the balance of risks.

- **FOMC_142_E02** — `fomcminutes20241107.pdf`, p. 12, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > In discussing the Committee’s statement, members agreed that it was appropriate to omit the previous reference to their greater confidence that inflation was moving sustainably toward 2 percent, as this language had been specifically associated with the commencement of policy easing in September and therefore was no longer needed. Almost all members agreed that the risks to achieving the Committee’s employment and inflation goals were roughly in balance. Members viewed the economic outlook as uncertain and agreed that they were attentive to the risks to both sides of the Committee’s dual mandate. In support of its goals, the Committee decided to lower the target range for the federal funds rate by 25 basis points to 4½ to 4¾ percent.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_143 · factual · test

**Question :** What distinct financial stability vulnerabilities did participants identify in the November 2024 FOMC minutes?

**Origine :** SUPP_2023_24 / Q21 · **Thème :** finance

- **FOMC_143_E01** — `fomcminutes20241107.pdf`, p. 10, année 2024, grade provisoire **2/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > In their discussion of financial stability, participants who commented noted vulnerabilities to the financial system that they assessed warranted monitoring. A couple of participants observed that the banking system was sound but that there continued to be potential risks associated with unrealized losses on bank assets. Many participants discussed vulnerabilities associated with CRE exposures, focusing on risks in the office sector. A few of these participants noted signs that the deterioration of conditions in this sector of the CRE market might be lessening.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_144 · comparative · dev

**Question :** How did commercial real estate lending standards evolve across the 2024 FOMC meeting reviews?

**Origine :** SUPP_2023_24 / Q22 · **Thème :** finance

- **FOMC_144_E01** — `fomcminutes20240131.pdf`, p. 6, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > In the January Senior Loan Officer Opinion Survey on Bank Lending Practices (SLOOS), banks reported tightening standards and terms on C&I loans to firms of all sizes over the fourth quarter. Regarding commercial real estate (CRE), banks reported tightening standards across all loan categories in the fourth quarter. Banks reported that they expected to keep lending standards unchanged for C&I loans and to tighten standards for CRE loans during 2024.

- **FOMC_144_E02** — `fomcminutes20240501.pdf`, p. 5, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > Banks reported tightening standards further in the April SLOOS for all loan categories of commercial real estate (CRE) loans. The growth of bank CRE loan balances slowed notably over the past year, reflecting the tightening of credit standards over this period, though growth of CRE loan balances picked up modestly in the first quarter.

- **FOMC_144_E03** — `fomcminutes20240731.pdf`, p. 5, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > Regarding commercial real estate (CRE) loans, banks in the July SLOOS reported tightening standards for all loan categories. Nonetheless, bank CRE loan balances increased over the second quarter, albeit at a diminished pace relative to the previous quarter.

- **FOMC_144_E04** — `fomcminutes20241107.pdf`, p. 6, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > In the October Senior Loan Officer Opinion Survey on Bank Lending Practices (SLOOS), banks, on net, reported maintaining their lending standards and most terms basically unchanged for C&I loans.2 Meanwhile, net growth in C&I loan balances remained subdued in August and September. With respect to commercial real estate (CRE) loans, banks in the October SLOOS reported, on balance, basically unchanged lending standards for all categories of CRE loans, the first survey since early 2022 in which standards on CRE loans of every category have not tightened. Bank CRE loan balances were flat in the third quarter, partly reflecting lending standards staying on the tighter end of the range prevailing since 2005. Credit remained available for most consumers, although consumer credit availability continued to tighten moderately through September.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## FOMC_145 · comparative · dev

**Question :** How did market-implied expectations for policy rate cuts shift between March and September 2024?

**Origine :** SUPP_2023_24 / Q24 · **Thème :** monetary_policy

- **FOMC_145_E01** — `fomcminutes20240320.pdf`, p. 3, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > The manager turned next to policy rate expectations. An estimate of the expected federal funds rate path derived from futures prices shifted up significantly over the intermeeting period. The modal federal funds rate path implied by options prices had also risen, but by substantially less than the futures-implied path. The move up in the futures-implied path reflected in part some shift in expectations toward policy rate cuts beginning later in the year, and cumulating to a smaller rate reduction in 2024, than previously assessed. Investors also appeared to have considerably lowered the perceived probability of more substantial rate cuts than in their baseline expectations. This lowering was evident in significantly more concentrated probability distributions for the federal funds rate over coming quarters. The changes in policy rate expectations over the intermeeting period occurred in the wake of stronger economic data, perceptions that disinflation might be proceeding more slowly than previously thought, and Federal Reserve communications. The median of modal paths of the federal funds rate obtained from the Open Market Desk’s Survey of Primary Dealers and Survey of Market Participants was also slightly higher. Responses still indicated substantial differences among survey participants in their assessments of the total amount of rate cuts likely to occur this year.

- **FOMC_145_E02** — `fomcminutes20240918.pdf`, p. 2, année 2024, grade provisoire **1/2** — SEMANTICALLY_PLAUSIBLE_NEEDS_HUMAN_CHECK

  > In the Open Market Desk’s Survey of Primary Dealers and Survey of Market Participants, most respondents had a modal expectation of a 25 basis point cut at this meeting, though the manager also noted that, since the time of the surveys—about a week earlier—the probability of a 50 basis point cut at the September meeting implied by futures prices had increased and exceeded the implied probability of a 25 basis point cut. The median respondent’s modal path for the federal funds rate shifted down notably over the next two years, in line with the options-implied modal path, and was unchanged thereafter. Balance sheet expectations in the surveys were little changed from July.

**À contrôler :** pertinence des différentes preuves; autres documents pouvant répondre; faits complémentaires requis; relecture humaine.

## Quand utiliser les variantes et les questions sans réponse ?

- **D’abord :** benchmark standard avec 145 requêtes (BM25, Dense, Hybride), sur 93 PDF. Après pooling et validation, figer les paramètres avec les splits.
- **Ensuite :** 30 formulations alternatives, en test de robustesse apparié, jamais réparties entre deux splits distincts. Mesurer la variation des métriques sans recalibrer chaque modèle sur les paraphrases du test.
- **Enfin :** 10 cas candidats sans réponse, après preuve documentaire de leur non-répondabilité. Pour un RAG, mesurer abstention, hallucinations et faux étayage. Ne pas les évaluer avec Recall@k de passages positifs.
