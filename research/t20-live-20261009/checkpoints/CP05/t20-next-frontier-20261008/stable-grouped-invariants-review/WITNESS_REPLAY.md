# Independent observation-to-moment witness replay

This is a synthetic integer histogram constructed from a chosen population law. No random groups were sampled, no physical observation was performed, and the full rational candidate list was not searched. The check below starts from the stored integer group-count frequencies rather than trusting the stored empirical moments.

M=3, C=2, R=4, w=1/4, delta=1/20. Chosen population support {1,3}, weights (2/7,5/7), survival 7/10.

Total synthetic groups: N=198517961374844800000000000.

For S=0,1,2,3,4, the integer frequencies are:

- N_0 = 26879453803604651082876432
- N_1 = 59460402558677125726798272
- N_2 = 58213752869418412930346592
- N_3 = 38383345622868648627406272
- N_4 = 15581006520275961632572432

They sum exactly to N. For order r, the factorial statistic equals binom(S,r)/binom(4,r). Therefore the histogram gives

hat m_r = [sum_(s=r)^4 N_s binom(s,r)] / [N binom(4,r)].

The independently recomputed integer numerators, denominators, and reduced moments are:

- r=1: 353361971247223744000000000 / 794071845499379200000000000 = 89/200
- r=2: 266849828859680128608000000 / 1191107768249068800000000000 = 44807/200000
- r=3: 100707371703972495157696000 / 794071845499379200000000000 = 25364801/200000000
- r=4: 15581006520275961632572432 / 198517961374844800000000000 = 15697326743/200000000000

These four fractions equal the chosen mixture moments (2/7)(7/10)^r+(5/7)(7/10)^(3r). This equality is deliberately engineered in the synthetic histogram, not claimed to be a likely exact outcome from random observations.

The sufficient fully rational group budget is 198517961374844625862262784, using the logarithm upper integer 8. The displayed total is at least this budget and satisfies 2 N tau^2 >= 8 while 2^8 >= 4C/delta.

The grid denominator is Q=56358560858112. Its weight numerators are (16102445959460, 40256114898652); its survival-grid index is h=33815136514867. Thus the actual grid candidate is

- weights (4025611489865/14089640214528, 10064028724663/14089640214528)
- survival 1/2+h/(3Q) = 118352977802035/169075682574336
- count support {1,3}, so primitive support (1,3) and zero flag false

Both weight and survival rounding are nonzero. The parameters satisfy the candidate weight floor w/2=1/8 and survival interval [1/2,5/6]. Direct rational recomputation from these grid parameters and the synthetic empirical moments gives the maximum discrepancy

8852412906385876589930580520871061427367819/1702485258699929879943808257148413706801545494605804339200

This is at most tau=1/7044820107264, and hence below the 2tau acceptance radius. A discrepancy-minimizing candidate cannot do worse, but no exhaustive minimizer was computed. The general selection and confidence claims rest on the theorem, not on this arithmetic witness.

Verdict: the complete stored synthetic observation histogram, observation-to-factorial transformation, budget check, candidate feasibility, and acceptance arithmetic all pass independent exact-rational replay.
