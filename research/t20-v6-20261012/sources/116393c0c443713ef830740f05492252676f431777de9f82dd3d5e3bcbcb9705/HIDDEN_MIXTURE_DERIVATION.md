# A nonattained infimum in the actual L1 evaluator

This is an ordinary exact all-horizon argument, with separate finite kernel checks. It is not claimed as a kernel proof of the infinite-law identity.

The new `hiddenMixturePacked` is a literal `P02.Codec.PackedProgram`, using only the original `Expr` and `Stmt` constructors. It leaves the existing evaluator, codec, invalid-index behavior, sentinel coding, measure and membership predicate unchanged. Its numeric index is the original `programIndex hiddenMixturePacked`.

`hiddenMixture_value` identifies the exact decoded evaluator output on every natural input:

    evaluateIndex (programIndex hiddenMixturePacked) n word
      = if n=0 then 0 else (((word / 2^n) mod 2) * (word mod 2)) mod 2.

For a sentinel-coded input prefix x_0,...,x_n, the first factor is x_0 and the second is x_n. Thus the actual synchronous output is y_0=0 and y_n=x_0 x_n for n>=1. Every stage reads only the available prefix and terminates.

Under the inherited fair independent Cantor input, conditional on x_0=0 the output is the zero stream. Conditional on x_0=1 the output is a fixed leading zero followed by an independent fair stream. Therefore the law is the injective prefix-zero pushforward of

    (1/2) delta_zero + (1/2) fairCantor.

The diffuse component has zero singleton masses and prefixing is injective. The only atom has mass exactly 1/2, so the original atomic mass is 1/2 and the original defect is 1/2.

At output horizon n>=1, the all-zero cylinder has mass 1/2+2^(-n). Every other nonempty output cylinder has mass 2^(-n), and has leading zero; cylinders starting with one have mass zero. At n=1 there is only the all-zero nonempty cylinder. For n>=2 the other cylinders have mass strictly below the heavy threshold 1/2. Consequently

    H(1,0)=1,
    H(1,n)=1/2+2^(-n) for n>=1,
    inf_n H(1,n)=1/2,
    H(1,n)>1/2 for every finite n.

Hence the tempting replacement `mass>r iff exists k, forall n, H(k,n)>r` fails at the exact actual numeric observer and r=1/2. The strict-cut theorem instead requires one rational slack witness t>r that is a lower bound at every horizon. No such t exists for this observer.

The finite kernel controls separately establish integer heavy counts 2,3,5,9 at horizons 1,2,3,4, and exact heavy mass 9/16 at horizon 4. They corroborate the ordinary all-horizon law argument; they do not replace it.

Credit: the root's `rational-threshold-root-controls-20261011/DERIVATION.md` supplied the half-point/half-fair measure counterexample. This file binds that existing control to the actual unchanged P02-L1 numeric evaluator through a harmless fixed prefix. No new arithmetical classification, philosophical consequence, integration, owner acceptance or T20 closure is claimed.
