import RationalRepairCertificate
open Orthemology.Tranche3
set_option maxRecDepth 4096
set_option maxHeartbeats 1000000

theorem generated_case_0 : rationalCertificate (0/1:ℚ) (253/256:ℚ) (0/1:ℚ) (0/1:ℚ) = (some (1/2:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_0 : RobustGood (0/1:ℚ) (253/256:ℚ) (0/1:ℚ) (0/1:ℚ) (1/2:ℚ) :=
  rationalCertificate_sound (0/1:ℚ) (253/256:ℚ) (0/1:ℚ) (0/1:ℚ) (1/2:ℚ) generated_case_0

theorem generated_case_1 : rationalCertificate (0/1:ℚ) (253/256:ℚ) (0/1:ℚ) (1/16:ℚ) = (some (1/2:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_1 : RobustGood (0/1:ℚ) (253/256:ℚ) (0/1:ℚ) (1/16:ℚ) (1/2:ℚ) :=
  rationalCertificate_sound (0/1:ℚ) (253/256:ℚ) (0/1:ℚ) (1/16:ℚ) (1/2:ℚ) generated_case_1

theorem generated_case_2 : rationalCertificate (0/1:ℚ) (253/256:ℚ) (1/10:ℚ) (0/1:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_3 : rationalCertificate (0/1:ℚ) (253/256:ℚ) (1/10:ℚ) (1/16:ℚ) = (some (27877/51200:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_3 : RobustGood (0/1:ℚ) (253/256:ℚ) (1/10:ℚ) (1/16:ℚ) (27877/51200:ℚ) :=
  rationalCertificate_sound (0/1:ℚ) (253/256:ℚ) (1/10:ℚ) (1/16:ℚ) (27877/51200:ℚ) generated_case_3

theorem generated_case_4 : rationalCertificate (0/1:ℚ) (253/256:ℚ) (1/4:ℚ) (0/1:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_5 : rationalCertificate (0/1:ℚ) (253/256:ℚ) (1/4:ℚ) (1/16:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_6 : rationalCertificate (3/256:ℚ) (1/1:ℚ) (0/1:ℚ) (0/1:ℚ) = (some (1/2:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_6 : RobustGood (3/256:ℚ) (1/1:ℚ) (0/1:ℚ) (0/1:ℚ) (1/2:ℚ) :=
  rationalCertificate_sound (3/256:ℚ) (1/1:ℚ) (0/1:ℚ) (0/1:ℚ) (1/2:ℚ) generated_case_6

theorem generated_case_7 : rationalCertificate (3/256:ℚ) (1/1:ℚ) (0/1:ℚ) (1/16:ℚ) = (some (1/2:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_7 : RobustGood (3/256:ℚ) (1/1:ℚ) (0/1:ℚ) (1/16:ℚ) (1/2:ℚ) :=
  rationalCertificate_sound (3/256:ℚ) (1/1:ℚ) (0/1:ℚ) (1/16:ℚ) (1/2:ℚ) generated_case_7

theorem generated_case_8 : rationalCertificate (3/256:ℚ) (1/1:ℚ) (1/10:ℚ) (0/1:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_9 : rationalCertificate (3/256:ℚ) (1/1:ℚ) (1/10:ℚ) (1/16:ℚ) = (some (27937/51200:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_9 : RobustGood (3/256:ℚ) (1/1:ℚ) (1/10:ℚ) (1/16:ℚ) (27937/51200:ℚ) :=
  rationalCertificate_sound (3/256:ℚ) (1/1:ℚ) (1/10:ℚ) (1/16:ℚ) (27937/51200:ℚ) generated_case_9

theorem generated_case_10 : rationalCertificate (3/256:ℚ) (1/1:ℚ) (1/4:ℚ) (0/1:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_11 : rationalCertificate (3/256:ℚ) (1/1:ℚ) (1/4:ℚ) (1/16:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_12 : rationalCertificate (201/4096:ℚ) (3895/4096:ℚ) (0/1:ℚ) (0/1:ℚ) = (some (1/2:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_12 : RobustGood (201/4096:ℚ) (3895/4096:ℚ) (0/1:ℚ) (0/1:ℚ) (1/2:ℚ) :=
  rationalCertificate_sound (201/4096:ℚ) (3895/4096:ℚ) (0/1:ℚ) (0/1:ℚ) (1/2:ℚ) generated_case_12

theorem generated_case_13 : rationalCertificate (201/4096:ℚ) (3895/4096:ℚ) (0/1:ℚ) (1/16:ℚ) = (some (1/2:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_13 : RobustGood (201/4096:ℚ) (3895/4096:ℚ) (0/1:ℚ) (1/16:ℚ) (1/2:ℚ) :=
  rationalCertificate_sound (201/4096:ℚ) (3895/4096:ℚ) (0/1:ℚ) (1/16:ℚ) (1/2:ℚ) generated_case_13

theorem generated_case_14 : rationalCertificate (201/4096:ℚ) (3895/4096:ℚ) (1/10:ℚ) (0/1:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_15 : rationalCertificate (201/4096:ℚ) (3895/4096:ℚ) (1/10:ℚ) (1/16:ℚ) = (some (223433/409600:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_15 : RobustGood (201/4096:ℚ) (3895/4096:ℚ) (1/10:ℚ) (1/16:ℚ) (223433/409600:ℚ) :=
  rationalCertificate_sound (201/4096:ℚ) (3895/4096:ℚ) (1/10:ℚ) (1/16:ℚ) (223433/409600:ℚ) generated_case_15

theorem generated_case_16 : rationalCertificate (201/4096:ℚ) (3895/4096:ℚ) (1/4:ℚ) (0/1:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_17 : rationalCertificate (201/4096:ℚ) (3895/4096:ℚ) (1/4:ℚ) (1/16:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_18 : rationalCertificate (2841/16384:ℚ) (13543/16384:ℚ) (0/1:ℚ) (0/1:ℚ) = (some (1/2:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_18 : RobustGood (2841/16384:ℚ) (13543/16384:ℚ) (0/1:ℚ) (0/1:ℚ) (1/2:ℚ) :=
  rationalCertificate_sound (2841/16384:ℚ) (13543/16384:ℚ) (0/1:ℚ) (0/1:ℚ) (1/2:ℚ) generated_case_18

theorem generated_case_19 : rationalCertificate (2841/16384:ℚ) (13543/16384:ℚ) (0/1:ℚ) (1/16:ℚ) = (some (1/2:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_19 : RobustGood (2841/16384:ℚ) (13543/16384:ℚ) (0/1:ℚ) (1/16:ℚ) (1/2:ℚ) :=
  rationalCertificate_sound (2841/16384:ℚ) (13543/16384:ℚ) (0/1:ℚ) (1/16:ℚ) (1/2:ℚ) generated_case_19

theorem generated_case_20 : rationalCertificate (2841/16384:ℚ) (13543/16384:ℚ) (1/10:ℚ) (0/1:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_21 : rationalCertificate (2841/16384:ℚ) (13543/16384:ℚ) (1/10:ℚ) (1/16:ℚ) = (some (895769/1638400:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_21 : RobustGood (2841/16384:ℚ) (13543/16384:ℚ) (1/10:ℚ) (1/16:ℚ) (895769/1638400:ℚ) :=
  rationalCertificate_sound (2841/16384:ℚ) (13543/16384:ℚ) (1/10:ℚ) (1/16:ℚ) (895769/1638400:ℚ) generated_case_21

theorem generated_case_22 : rationalCertificate (2841/16384:ℚ) (13543/16384:ℚ) (1/4:ℚ) (0/1:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_23 : rationalCertificate (2841/16384:ℚ) (13543/16384:ℚ) (1/4:ℚ) (1/16:ℚ) = (some (158489/262144:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_23 : RobustGood (2841/16384:ℚ) (13543/16384:ℚ) (1/4:ℚ) (1/16:ℚ) (158489/262144:ℚ) :=
  rationalCertificate_sound (2841/16384:ℚ) (13543/16384:ℚ) (1/4:ℚ) (1/16:ℚ) (158489/262144:ℚ) generated_case_23

theorem generated_case_24 : rationalCertificate (19597/65536:ℚ) (45939/65536:ℚ) (0/1:ℚ) (0/1:ℚ) = (some (1/2:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_24 : RobustGood (19597/65536:ℚ) (45939/65536:ℚ) (0/1:ℚ) (0/1:ℚ) (1/2:ℚ) :=
  rationalCertificate_sound (19597/65536:ℚ) (45939/65536:ℚ) (0/1:ℚ) (0/1:ℚ) (1/2:ℚ) generated_case_24

theorem generated_case_25 : rationalCertificate (19597/65536:ℚ) (45939/65536:ℚ) (0/1:ℚ) (1/16:ℚ) = (some (1/2:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_25 : RobustGood (19597/65536:ℚ) (45939/65536:ℚ) (0/1:ℚ) (1/16:ℚ) (1/2:ℚ) :=
  rationalCertificate_sound (19597/65536:ℚ) (45939/65536:ℚ) (0/1:ℚ) (1/16:ℚ) (1/2:ℚ) generated_case_25

theorem generated_case_26 : rationalCertificate (19597/65536:ℚ) (45939/65536:ℚ) (1/10:ℚ) (0/1:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_27 : rationalCertificate (19597/65536:ℚ) (45939/65536:ℚ) (1/10:ℚ) (1/16:ℚ) = (some (3591309/6553600:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_27 : RobustGood (19597/65536:ℚ) (45939/65536:ℚ) (1/10:ℚ) (1/16:ℚ) (3591309/6553600:ℚ) :=
  rationalCertificate_sound (19597/65536:ℚ) (45939/65536:ℚ) (1/10:ℚ) (1/16:ℚ) (3591309/6553600:ℚ) generated_case_27

theorem generated_case_28 : rationalCertificate (19597/65536:ℚ) (45939/65536:ℚ) (1/4:ℚ) (0/1:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_29 : rationalCertificate (19597/65536:ℚ) (45939/65536:ℚ) (1/4:ℚ) (1/16:ℚ) = (some (642189/1048576:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_29 : RobustGood (19597/65536:ℚ) (45939/65536:ℚ) (1/4:ℚ) (1/16:ℚ) (642189/1048576:ℚ) :=
  rationalCertificate_sound (19597/65536:ℚ) (45939/65536:ℚ) (1/4:ℚ) (1/16:ℚ) (642189/1048576:ℚ) generated_case_29

theorem generated_case_30 : rationalCertificate (475667/1048576:ℚ) (572909/1048576:ℚ) (0/1:ℚ) (0/1:ℚ) = (some (1/2:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_30 : RobustGood (475667/1048576:ℚ) (572909/1048576:ℚ) (0/1:ℚ) (0/1:ℚ) (1/2:ℚ) :=
  rationalCertificate_sound (475667/1048576:ℚ) (572909/1048576:ℚ) (0/1:ℚ) (0/1:ℚ) (1/2:ℚ) generated_case_30

theorem generated_case_31 : rationalCertificate (475667/1048576:ℚ) (572909/1048576:ℚ) (0/1:ℚ) (1/16:ℚ) = (some (1/2:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_31 : RobustGood (475667/1048576:ℚ) (572909/1048576:ℚ) (0/1:ℚ) (1/16:ℚ) (1/2:ℚ) :=
  rationalCertificate_sound (475667/1048576:ℚ) (572909/1048576:ℚ) (0/1:ℚ) (1/16:ℚ) (1/2:ℚ) generated_case_31

theorem generated_case_32 : rationalCertificate (475667/1048576:ℚ) (572909/1048576:ℚ) (1/10:ℚ) (0/1:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_33 : rationalCertificate (475667/1048576:ℚ) (572909/1048576:ℚ) (1/10:ℚ) (1/16:ℚ) = (some (57623059/104857600:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_33 : RobustGood (475667/1048576:ℚ) (572909/1048576:ℚ) (1/10:ℚ) (1/16:ℚ) (57623059/104857600:ℚ) :=
  rationalCertificate_sound (475667/1048576:ℚ) (572909/1048576:ℚ) (1/10:ℚ) (1/16:ℚ) (57623059/104857600:ℚ) generated_case_33

theorem generated_case_34 : rationalCertificate (475667/1048576:ℚ) (572909/1048576:ℚ) (1/4:ℚ) (0/1:ℚ) = (some (10437139/16777216:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_34 : RobustGood (475667/1048576:ℚ) (572909/1048576:ℚ) (1/4:ℚ) (0/1:ℚ) (10437139/16777216:ℚ) :=
  rationalCertificate_sound (475667/1048576:ℚ) (572909/1048576:ℚ) (1/4:ℚ) (0/1:ℚ) (10437139/16777216:ℚ) generated_case_34

theorem generated_case_35 : rationalCertificate (475667/1048576:ℚ) (572909/1048576:ℚ) (1/4:ℚ) (1/16:ℚ) = (some (10437139/16777216:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_35 : RobustGood (475667/1048576:ℚ) (572909/1048576:ℚ) (1/4:ℚ) (1/16:ℚ) (10437139/16777216:ℚ) :=
  rationalCertificate_sound (475667/1048576:ℚ) (572909/1048576:ℚ) (1/4:ℚ) (1/16:ℚ) (10437139/16777216:ℚ) generated_case_35

theorem generated_case_36 : rationalCertificate (49/100:ℚ) (51/100:ℚ) (1/10:ℚ) (0/1:ℚ) = (some (5499/10000:ℚ)) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_sound_36 : RobustGood (49/100:ℚ) (51/100:ℚ) (1/10:ℚ) (0/1:ℚ) (5499/10000:ℚ) :=
  rationalCertificate_sound (49/100:ℚ) (51/100:ℚ) (1/10:ℚ) (0/1:ℚ) (5499/10000:ℚ) generated_case_36

theorem generated_case_37 : rationalCertificate (-1/1:ℚ) (1/1:ℚ) (0/1:ℚ) (0/1:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_38 : rationalCertificate (0/1:ℚ) (1/1:ℚ) (1/3:ℚ) (1/1:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

theorem generated_case_39 : rationalCertificate (3/4:ℚ) (1/4:ℚ) (1/10:ℚ) (1/1:ℚ) = none := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]

#print axioms generated_case_0
#print axioms generated_sound_0
