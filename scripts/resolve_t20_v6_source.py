#!/usr/bin/env python3
"""Resolve preserved source identities and reconstruct a qualified isolated suite.

This tool copies verified sources; it does not execute historical wrappers or
certify scientific acceptance. Same-named historical variants stay separate.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import os
import pathlib
import re
import stat
import struct
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
PREFIX = 'research/t20-v6-20261012'
PUBLIC = {'ADD_EXACT', 'PROJECT', 'REUSE'}
CURRENT_GRAPH_SHA256 = 'ce15fabe3966d210aadbbf51b0d1213c45d6f9397a3dfebbaa66257afc32b5ff'

# A finite current-copy class, separate from historical prose recovery. Its
# members are derived from existing frozen maps, not a second path catalogue.
CONTINUATION_COPY_ROOT = 'experiments/orthemology-v5-continuations/source-store/'
CONTINUATION_RETAINED_ROOT = 'experiments/orthemology-v5-successors/source-store/'
CONTINUATION_COPY_BASE = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
CONTINUATION_LEGACY_BASE = '19de267cd41d2a5eeeb3eaf0b91562f706e2a916'
CONTINUATION_COPY_COUNT = 258
CONTINUATION_COPY_EXCLUDED = 'b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183'
CONTINUATION_COPY_METADATA = {'docs/provenance/v5-research-continuations/SOURCE_MAP.json': (5942902,
                                                               'e7cce0f3ad6c7742ea2b3702963dfad8920e06e3f1208f15656d926922e64725'),
 'docs/provenance/v5-successors/SOURCE_MAP.json': (4978847,
                                                   'db90ad110ccc9c6a63454cf91ecec4605eed7fe243d18883d3cf501c58cb4883'),
 'docs/provenance/v5-successors/PRESERVATION.json': (379708,
                                                     'cd81d3b80d5183c1c01b637207d0afefd2b143ce4ee346808ca473a15eea6c4a')}


# Finite public document/evidence copies at distinct checkpoint coordinates.
# Exact bodies remain in the selected checkpoint; dates and old review validity
# stay attached to the requested original coordinate. No scientific/B credit or
# historical-wrapper execution follows from this reusable resolver route.
CHECKPOINT_COPY_ROOT = 'research/t20-live-20261009/checkpoints/'
CHECKPOINT_COPY_BASE = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
CHECKPOINT_COPY_MEMBERS = (
    ('CP04', 'CP01', 't20-next-frontier-20261008/formal-identification/DEPENDENCY_MANIFEST.json',
     '92a8049abc1f1b43ae2b4a6605616034f0dd2682', '5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752', 2786),
    ('CP03', 'CP01', 't20-next-frontier-20261008/formal-route-probability/KERNEL_STATUS.json',
     'bb052b92891889a79973ee7904e24674a3c7f549', 'fe7d51f3778d2fc071ee7991a2ce6adcc98aa3d4a4cbdb9ce4ce0b950b757bbb', 2109),
    ('CP05', 'CP04', 't20-next-frontier-20261008/global-calibration-ambiguity/POLYNOMIAL_EFFICIENCY_APPENDIX.md',
     '323b35e3a4827ab25416d551c84372cf88b11ed7', '4242d8cbcc9fd576266e2ee01f902b45c93e6701b5c01d07a5a0c3909f97f0f4', 7854),
    ('CP05', 'CP04', 't20-next-frontier-20261008/multi-root-adaptive-bound/RESULT.md',
     '0e36c9ded80d8dd66672cf9fede89f2b9d551ad5', '60f7f240fc98d2105bddf0d4668f6e1a18e81df62421f333a4b92da3ff5f2a00', 12090),
    ('CP13', 'CP04', 't20-next-frontier-20261008/root-next-operations/AKMALIYYA_SCOPE_RETURN.json',
     'f7f46c2d4b4ac09dded46f1bac6001c701dc2263', '6f59482cf6770b254af3e57a77a47ae36fbd1958be33a3f7e44800f03673eb78', 1105),
    ('CP13', 'CP04', 't20-next-frontier-20261008/root-next-operations/MAJMU_DETERMINATION_RETURN.json',
     'eee93d868027b3005a7d7dbab4d8458ab5bfa894', '69d02a0c84c36344e6dc693372dd3a8ecb53745f9c01cca41ecf03e2c6b93e48', 1019),
    ('CP06', 'CP05', 't20-next-frontier-20261008/grouped-calibration-invariants/RESULT.md',
     '8510ca89507c6c5e367b095eb5c57ed9156bda22', 'c47fd19a08eba9e3ae18885c264b45285defca4ae34e33db60e786385aa82113', 17594),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction-review/ERRATUM.md',
     'ff7cebe6d5d12029bfa5d091cbecede107192b9c', '8ed2d479c07d30487072ba0b5dde52228259cb88589ec295de73453f5b3bc9f1', 1492),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction-review/ERRATUM_RECEIPT.json',
     '93a4d5f1f79609706365260cd85d8331ee7195f4', '34932c23d76203b90f6f569067d588bce66ad3e222018543a241eca4202a02ab', 2239),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction-review/INDEPENDENT_CONTROLS.json',
     'cdbfd3383a0496b14ee46d08cb49bbe02ee77c3c', 'c4f01971fcc1b5c31a4a36bd47642554221ba4217f38355e07bd45a2667aa353', 857),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/independent/INDEPENDENT_CONTROLS.json',
     'cdbfd3383a0496b14ee46d08cb49bbe02ee77c3c', 'c4f01971fcc1b5c31a4a36bd47642554221ba4217f38355e07bd45a2667aa353', 857),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction-review/REVIEW.md',
     '1a6317993fe9a2125165b6796b9ac222258f1f0d', '85284366281cc77a4957ddf8b291d5a91c641fa9e80ce0889eb94a2062460dbf', 12195),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction-review/REVIEW_MANIFEST.json',
     '3314fa90dcf9fa3c6919e3b161838898975bcab8', '6bc8b43fbf0f91812c8344475857d0db7430fa553fb2d365cf4ee8af2d2889ec', 2831),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction-review/VERIFICATION.json',
     '53b1194884c22420c89aad38cd6fb9eeff0e5870', '9d7fff67839a3f665517cfb813359e64e4d91498d55df453e38f5bda315f254f', 412),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction/results/review_verification.json',
     '53b1194884c22420c89aad38cd6fb9eeff0e5870', '9d7fff67839a3f665517cfb813359e64e4d91498d55df453e38f5bda315f254f', 412),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction-review/author_replay/results/exact_controls.json',
     'e37fa1d113849f5f5e89685ba0556ceb4b975e0c', '86b3c4bc0bba32cf1845d6768df85565404c6f197c556d79fe4935fb55d441d6', 1156),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/author/results/exact_controls.json',
     'e37fa1d113849f5f5e89685ba0556ceb4b975e0c', '86b3c4bc0bba32cf1845d6768df85565404c6f197c556d79fe4935fb55d441d6', 1156),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction/results/exact_controls.json',
     'e37fa1d113849f5f5e89685ba0556ceb4b975e0c', '86b3c4bc0bba32cf1845d6768df85565404c6f197c556d79fe4935fb55d441d6', 1156),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction/EXACT_CONTROLS.md',
     '26fbe5cab7b5ecc117da1a549ea1e0722c87de97', '1d56ba9524576b64dc9cdcb56a611247cfa316db424fe3b750a3c44c239e5e4a', 1614),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction/MANIFEST.json',
     'd244623a7a1d3e5150ec0e61fe193249e125e30f', 'cc3e64188ba50ef51c1652d9989616d487ea4c7498673e13b3493a0cb06bd2df', 3462),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction/READ_FIRST.md',
     'a483d1f645023250d69f6768ca882f10897a1873', '557dafd62477f2f4341cdf50122dc1cb6b2ac37ea86225e7362818691d9009ba', 1229),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction/RESULT.md',
     '93080c5e116ccf3354be9c6f839b102cf2010e70', 'f8424612e92e5f4f3d45f89317070bf5ed4fd63b5cc53a43ee88b4713bc29f4b', 12481),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction/REVIEW_STATUS.md',
     '7962bb34603a67c8ef9d5cbdc93baeb541a0ad32', '872e2c09030b2170609d72fbbae093c1de834e98d36085cd1b44cae01d96982b', 2516),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction/SOURCE_BINDINGS.json',
     '38ae078a500621a0ec31526b6ab31b3c008b13f6', 'ec2f86038126da0bf98ed994982341adc1cf58fa2807707979baf217c1612888', 20571),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction/results/erratum_verification.json',
     '14716e4a32662509e3009f6ad7f76f22be7762a2', 'b9cc706acd6b7b90e4dfbd759a26a1d7796e65672802cf2cf908eb42cf9451d6', 425),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-absence-obstruction/results/verification.json',
     '67199d34e76f1bf30c5d4d0348a3b7c05828b9e4', 'ac760e3b59e2daed2221b1ca38f500181f96c8801f4ce1b3287a24dacc7bbbd6', 278),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/APPENDIX_REVIEW_RECEIPT.json',
     'bfcf27cf2734aeafab994beb7b72fde3c48166a2', 'f8ee9578c1712159f9a380e003d69e83fe55185c462e8fbff44ba19ba1e9159e', 2960),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/AUTHOR_BINDING.json',
     '041b5d98e00ae1e582f6c782d09b271beca1426e', '9a811327a71fac45577450534b1c89606ee6d355ba9e82fbf48ea51859e6a37b', 3004),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/FINAL_VERIFICATION.json',
     '0fdf9089c56ded8c5a48801b27529b4311c8e27c', 'b5e520b7b0edb4e8e68843e80c3d6d7760337e8283dd33753b557cf7772d6ad8', 676),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor/results/review_verification.json',
     '0fdf9089c56ded8c5a48801b27529b4311c8e27c', 'b5e520b7b0edb4e8e68843e80c3d6d7760337e8283dd33753b557cf7772d6ad8', 676),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/FINITE_PANEL_REVIEW.md',
     'b1eacb228abbc93e2542690b5d9916d750a4598c', 'd16ed278ce739bf88fad955282d76596a636760f634e2d182c95ff28a173dc6f', 6415),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/INDEPENDENT_CONTROLS.json',
     '62cd1fa163ef6963ef0585e537e80ae72b62f469', '59c86afedadd911205bb5268d65103c372c6deee908df716ef9df8e4e9de0d3c', 1029),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/INDEPENDENT_PANEL_CONTROLS.json',
     '64fd6ee077de16bc89ecc4de43e82fabb7d0b5e8', 'd6e5e864eda7261803ae606c0685267669d72b2e9081a8b8c39f7c4b67c25cb0', 453),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/MAIN_REVIEW_RECEIPT.json',
     'ae1a401ac4817971b7ce8b08b4d07f71894182f0', 'd85b5f1b18651d29c1db0f5f4ffeb18bf9f76e7c851f942d2ff13cef9700ce45', 2588),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/REVIEW.md',
     'bc9371a14344f6a1d5fcb43a642a19dacec566d3', 'f3e84991aaa17f1438df141f7227ab6a763d67d4a5c28fb1b67575da14dcaf71', 12365),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/REVIEW_MANIFEST.json',
     '1719e95c4b0ba1ad05b7ce96560976172df01d80', '5441a2231dfeee1a71e1aa9204c1bc75b8496c9c6cc4608b03a1065e3bdfe359', 5346),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/results/exact_controls.json',
     'c650b2ed1a53b797ccf8380720426f4d322193d4', '5720a0aab8d45828c14245d89381348af73842e6a44ff7cadd9e7dc6771ebff1', 1076),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/results/exact_controls.json',
     'c650b2ed1a53b797ccf8380720426f4d322193d4', '5720a0aab8d45828c14245d89381348af73842e6a44ff7cadd9e7dc6771ebff1', 1076),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/results/exact_controls.json',
     'c650b2ed1a53b797ccf8380720426f4d322193d4', '5720a0aab8d45828c14245d89381348af73842e6a44ff7cadd9e7dc6771ebff1', 1076),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor/results/exact_controls.json',
     'c650b2ed1a53b797ccf8380720426f4d322193d4', '5720a0aab8d45828c14245d89381348af73842e6a44ff7cadd9e7dc6771ebff1', 1076),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/results/panel_controls.json',
     '95b534ad24631d7ae3d8add40591b286ea6c101d', '4467534cca35cd63de8f3d0bfd45cbef5cfcdd8948f779c8af41cc402c7500a7', 535),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/results/panel_controls.json',
     '95b534ad24631d7ae3d8add40591b286ea6c101d', '4467534cca35cd63de8f3d0bfd45cbef5cfcdd8948f779c8af41cc402c7500a7', 535),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/results/panel_controls.json',
     '95b534ad24631d7ae3d8add40591b286ea6c101d', '4467534cca35cd63de8f3d0bfd45cbef5cfcdd8948f779c8af41cc402c7500a7', 535),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor/results/panel_controls.json',
     '95b534ad24631d7ae3d8add40591b286ea6c101d', '4467534cca35cd63de8f3d0bfd45cbef5cfcdd8948f779c8af41cc402c7500a7', 535),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/EXACT_CONTROLS.md',
     '57f2b99cbc5fda63b5da3dd59d6bb9317f1ef72a', 'b30ea170c53b94cc6a8bf9f41cae0fd4840965d4519542c006c94506017b888c', 2210),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor/EXACT_CONTROLS.md',
     '57f2b99cbc5fda63b5da3dd59d6bb9317f1ef72a', 'b30ea170c53b94cc6a8bf9f41cae0fd4840965d4519542c006c94506017b888c', 2210),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/FINITE_PANEL_APPENDIX.md',
     '63a1c424dec9dd07651388b7bef35c55d050e436', 'f3a18659ad08546714ad2db3aeb30e344d149eac944b3bd0bb8d62508375d2e4', 8194),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor/FINITE_PANEL_APPENDIX.md',
     '63a1c424dec9dd07651388b7bef35c55d050e436', 'f3a18659ad08546714ad2db3aeb30e344d149eac944b3bd0bb8d62508375d2e4', 8194),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/READ_FIRST.md',
     '6ec3739d7f8041774b0a6833c57625b6319fbca5', '56468e1e3a00f85dbbf2f1e7dd0ca26940e5747603c431c18659f014c176f688', 1553),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor/READ_FIRST.md',
     '6ec3739d7f8041774b0a6833c57625b6319fbca5', '56468e1e3a00f85dbbf2f1e7dd0ca26940e5747603c431c18659f014c176f688', 1553),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/RESULT.md',
     'e631f2dab46506d48cfc2768f5309ae0ef95655e', '827b5e66f8bf689ed4c0c4de525163b2d14fde3a2c23f25ecc297b53daee8bc3', 15546),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor/RESULT.md',
     'e631f2dab46506d48cfc2768f5309ae0ef95655e', '827b5e66f8bf689ed4c0c4de525163b2d14fde3a2c23f25ecc297b53daee8bc3', 15546),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/SOURCE_AUDIT.md',
     '659eebbe5efe9d41589672e9f1cb028522d4db8c', '439a9c0e893dbee30a2e24ea555788251e76fee7e5dd060cfa88049156edf8b6', 6901),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/SOURCE_BINDINGS.json',
     'fc8c70e78349328bc98d6318db713e832558b905', 'd295a32a9051db9540980bda48781dcd10e66a3bf9a6ec453f2f976edbe8eb17', 11953),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor/SOURCE_BINDINGS.json',
     'fc8c70e78349328bc98d6318db713e832558b905', 'd295a32a9051db9540980bda48781dcd10e66a3bf9a6ec453f2f976edbe8eb17', 11953),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor/MANIFEST.json',
     '4d574799eb9bf90ca5a4c3b0f4994679b1d1e8ae', '5cceea13e65e76604e1290ab420a34bb352c506c73d2f65937afdd10bdd6005b', 4029),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor/REVIEW_STATUS.md',
     'b74e769bd095a7809527c76d7b013ece4d22f0f1', '37473e32858ec1b1fb69f7ac5e49afa5d898d0bd5da95750685acb220d9fec94', 2582),
    ('CP06', 'CP05', 't20-next-frontier-20261008/interaction-calibration-anchor/results/verification.json',
     '2202cf96d0507fb9f54c239e9935598728a08c7e', '750e23242eeb2db97affa8c4aaea5a9fdd5469f1f2e907fa8096407923a2fcdf', 503),
    ('CP07', 'CP06', 't20-next-frontier-20261008/dependent-gate-transport/results/exact_controls.json',
     '82b17f1be444762f878b42d51bd80de8e18afca8', 'cb68c4936ac039a7046a411d717078e1212006fbabb0fd8620ef98bf679779db', 18639),
    ('CP07', 'CP06', 't20-next-frontier-20261008/dependent-gate-transport/ADDENDUM_MANIFEST.json',
     'b26b256e1ab852a5ad6a0b595532763f3bd9aee4', '66a631d04cfe92964aaf8829f3668e362b589004d1c1c66dba287c4155513716', 467),
    ('CP07', 'CP06', 't20-next-frontier-20261008/dependent-gate-transport/EXACT_CONTROLS.md',
     'e8b96357ec740364aec9356f55259e0350d48ca2', '463b14ece2b32e3004c9c9bc373664803a6daa81ee6e20210406a849808261fc', 2062),
    ('CP07', 'CP06', 't20-next-frontier-20261008/dependent-gate-transport/MANIFEST.json',
     'f94d329e41ab0f1327b1a375dd08d45fb16f5b40', '3ef066a690d014d22bfafb4cadb40e3506ead0c2f576b98345ab42da46af0661', 1809),
    ('CP07', 'CP06', 't20-next-frontier-20261008/dependent-gate-transport/READ_FIRST.md',
     '2ca62541455a1ad8390cd643bd4aa613172021ce', '48ae64facbc6556c6f4346858f74a3a0f0049077c9d11e9adfbb0fc8c0d05be4', 1231),
    ('CP07', 'CP06', 't20-next-frontier-20261008/dependent-gate-transport/RESULT.md',
     'd9b737b26933106a0b9d1514885258615f1be0ff', 'b32125f6d4fc8a715e18b5f0761e3be88b8194d1f4db58f088cfc2df122ce997', 15467),
    ('CP07', 'CP06', 't20-next-frontier-20261008/dependent-gate-transport/SEMANTIC_GUARD.md',
     '50b87abf2aff6f5ea1294687d94c501a9e3d4170', '0fbd40f05cb115621d367a220eb1bdc754a218e6fd6b84f8d5e4c63af8dbd924', 1792),
    ('CP07', 'CP06', 't20-next-frontier-20261008/same-threshold-replay/results/predecessor_verification.json',
     '8d804c7a822234df208caa44f61835c70cdd3b59', 'bebb17eace4e5bed8431fa6d8daed38d92c53ec568c7557cf22b2eac60e1c817', 556),
    ('CP07', 'CP06', 't20-next-frontier-20261008/dependent-gate-transport/sources/SOURCE_READS.json',
     'e88f37581b9259c0edffe71f44d6752d260eda78', 'dae0993624569e077dd96def3e52d243b222f0dd5a6a94475a05cc5115d195b5', 2114),
    ('CP07', 'CP06', 't20-next-frontier-20261008/finite-panel-replay-review/REVIEW.md',
     '033912a360b57693eec8f1b6239f1de91fedaf5f', '812eb02988e1e2e695e71fcdead1debbd20a9525570b5f3eb68c26b601af208e', 6960),
    ('CP07', 'CP06', 't20-next-frontier-20261008/finite-panel-replay/EVENT_RECORD.json',
     '6f7c98e13eca8c7fc7cebfaf1c2c443d35446e3a', '1537019ced01d70638a737127261845249ab7b53860001f2cb335a6b4801f1ae', 1251),
    ('CP07', 'CP06', 't20-next-frontier-20261008/finite-panel-replay/RESULT.md',
     '54297711cd24a7e59f019ca0382cf6788907dffb', '327b6fb25944ac90e7ecd6010a427993b69400fbdc9b79928d731120b6d62243', 10261),
    ('CP07', 'CP06', 't20-next-frontier-20261008/finite-panel-replay/SHARED_MARGINAL_BOUNDARY.md',
     '214d278965e132cbee093e92c36e11d969c3b25c', '3d55f739d398ed1b4b28253cdb5db34ec9b32d46415e14750a612e35f43b4788', 3986),
    ('CP07', 'CP06', 't20-next-frontier-20261008/finite-panel-replay/SOURCE_REVIEW_BINDINGS.md',
     'ced42397e41ed9cec02f1c6a58a98bc52ab370ab', '83df5ebbbf0717d09392af28d5a7ca77fcfc783dc7f13484c586d157d086faac', 3082),
    ('CP07', 'CP06', 't20-next-frontier-20261008/finite-panel-replay/VERIFICATION.md',
     'd3f67a26881b8669d3ed7b2c710ae89ee48ff6b8', '6a335e09623ae4d446a0f820b37862077dd3903cec3d6ceeb31fac17c34ad279', 1946),
    ('CP07', 'CP06', 't20-next-frontier-20261008/same-threshold-replay/results/exact_controls.json',
     '9eed1cbf88853aafd60ab5ac7f1ef5e1a3f2bf04', '060ed3aae850901e96d00a59b2b42f10e7c3e933628cd97e7503b8368b656596', 3717),
    ('CP07', 'CP06', 't20-next-frontier-20261008/same-threshold-replay/EXACT_CONTROLS.md',
     '866c86207fc0fe53f44ea7c3f26312fe487b9a3d', 'f0f438a4f99c5a2fef5b7f40384747c46f1454cfb1b719b4cb96dd6fa1d9b16b', 1767),
    ('CP07', 'CP06', 't20-next-frontier-20261008/same-threshold-replay/MANIFEST.json',
     'f0b00ac183c7dff1bd3fe8e3eb672be27947ebc5', 'f58c75e855e51be1bf4818b2b4ea6a91b1b5e685cbd45cfe304e9c3627fcbf53', 1857),
    ('CP07', 'CP06', 't20-next-frontier-20261008/same-threshold-replay/READ_FIRST.md',
     '9ffcabad480480e24fe68313b6c4f415d8fa650b', 'ecae3eedf6b01f76bd31b039826c932f5418e9d3cf3a5679826c18f4dcf6a641', 1522),
    ('CP07', 'CP06', 't20-next-frontier-20261008/same-threshold-replay/RESULT.md',
     '16eca5efce18c796fcc7e5493841cb00967aadbc', 'f3c9b2690613e5c0abd7f5e188f01abcff9aa37380a14c8eac4fe428e7df7098', 15218),
    ('CP09', 'CP06', 't20-next-frontier-20261008/same-threshold-replay/RESULT.md',
     '16eca5efce18c796fcc7e5493841cb00967aadbc', 'f3c9b2690613e5c0abd7f5e188f01abcff9aa37380a14c8eac4fe428e7df7098', 15218),
    ('CP08', 'CP07', 't20-next-frontier-20261008/arbitrary-face-replay-design-review/UNIFORM_BOUND_AND_SHARP_ASYMPTOTICS.md',
     'e802402e21d5f98610d3a7094a1e904631f19c19', '1543ed1b1406bd59948bd66f962001f451dbff2523e3f0e8b67a96a82ad319e9', 12931),
    ('CP08', 'CP07', 't20-next-frontier-20261008/arbitrary-face-replay-design/ASYMPTOTIC_DESIGN.md',
     'e28f8620513530ba1216a815cc6ae3d535ea4623', 'c2f454fa409f16befc6603954a070286bf7640e56c7fddddbcc6a51ef6e3651c', 5833),
    ('CP09', 'CP07', 't20-next-frontier-20261008/arbitrary-face-replay-design/ASYMPTOTIC_DESIGN.md',
     'e28f8620513530ba1216a815cc6ae3d535ea4623', 'c2f454fa409f16befc6603954a070286bf7640e56c7fddddbcc6a51ef6e3651c', 5833),
    ('CP09', 'CP08', 't20-next-frontier-20261008/adaptive-two-face-corollary/RESULT.md',
     '5eda366c1c0240a662fbf9c051cea85766a4a169', '3997cb39f8306545ac622feeb19e55f0fe18c570e0059e84dea39940c6b22e0f', 9589),
    ('CP13', 'CP08', 't20-next-frontier-20261008/root-later-operations/DASGUPTA_TARGETED_RETURN.json',
     '4e1e3b8afad4e90a0b62911d3a35345f38b115dc', '60c9139f0fd7110127d2f844ebad9e51ec7a6b5369f2f8fedd1c7d20f429d4f6', 1878),
    ('CP15', 'CP14', 't20-next-frontier-20261008/root-later-operations/COMMON_SOURCE_REASSESSMENT_AFTER_REDUNDANCY_20261009.md',
     'ed0a1874421e0d3ccd7d6c058b7fc25f07741c83', '4f982bebd1c4add817a93a1445407a31374dc9f42d056e987bb14f816f17d9d1', 8405),
    ('CP15', 'CP14', 't20-next-frontier-20261008/root-later-operations/COMMON_SOURCE_REASSESSMENT_FRONTIER_20261009.json',
     '0059e1fe9a521f6bb4a7ecd138ab52c10edc9be3', '728d77288829abcd8cc2a940d9448d48c4545c0c1becae8e14a2c97c9fc61429', 1804),
    ('CP15', 'CP14', 't20-next-frontier-20261008/root-later-operations/ONENESS_WARRANT_JUDGEMENT_20261009.md',
     '77148dc9702fe0378cce8090d2eeec136a82dd8b', 'd45920d6306244db723caa6ad6cbb13aab8f12890af32912353a86388d7d58f1', 5830),
)
CHECKPOINT_COPY_CATALOG_SHA256 = '85c5eb6585d6846b12b85e556ee1126748db23dd3313145d2c5846f9a4ea9d55'
CHECKPOINT_COPY_PATHS = frozenset(CHECKPOINT_COPY_ROOT + checkpoint + '/' + member
    for checkpoint, retained, member, blob, identity, size in CHECKPOINT_COPY_MEMBERS)


# Exactly reviewed historical-only prose, not a suffix/directory exemption.
# Ordinary reading uses the existing recognition chapter; original identities
# and the duplicate CP20 proof occurrence remain independently authenticated.
# Finite recorded outputs whose exact bytes survive at named public providers.
# Requested coordinates retain their historical context; this grants no replay,
# scientific acceptance, independent review, category credit or deletion right.
CHECKPOINT_RECORD_COPY_MEMBERS = (
    ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/identification-review/results/INDEPENDENT_METRICS_V2.json',
     'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/identification-review/results/INDEPENDENT_METRICS.json',
     'f89629abfbaea7adb57d146681d26a4c94ea5c33', 'fbdc2e9d069dd57b7989b1ae41e37f8190f7eb7194b06ba9339a2eccd871fbf7', 517),
    ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/wise-determination/results/TRANSPORT_PARENT_REPLAY.json',
     'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/wise-determination/review/transport_results.json',
     'ddeff05d24dd5c1378367a5a9e473d8fea250ffb', 'c2fdf5f473ae028e809ab067e584b44cdd7855e94391c8175c503979f91d40a0', 3507),
    ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/results/AUTHOR_FINAL_MANIFEST.json',
     'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/MANIFEST.json',
     '5ce74ffe98f18124374a1c1bf969490b660780d2', '43681d0c2d070e30200afb7b3dc557396150bff9c8012e75bd0a72328a27a974', 5653),
    ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/grouped-mixture-identification/MANIFEST.json',
     'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/grouped-mixture-review/frozen/MANIFEST.json',
     '205957502d0d172596cf3628bfbe7331e323da03', 'baf29c6df8ba1047782a03f794409bf03a0bfe8394f04845bb2b876b6bcc75f6', 1575),
    ('research/t20-live-20261009/checkpoints/CP03/t20-next-frontier-20261008/catalogue-mixture-review/frozen/MANIFEST.json',
     'research/t20-live-20261009/checkpoints/CP03/t20-next-frontier-20261008/catalogue-mixture-sampling/MANIFEST.json',
     '2da194a85f3b2419b9e1bb205b64cee5be6e681c', '4cc3ee6c2eef3ea291e020bd3a62638694c2ed3f492ad32519cb4fb3a3932ea1', 1943),
    ('research/t20-live-20261009/checkpoints/CP03/t20-next-frontier-20261008/catalogue-mixture-review/frozen/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP03/t20-next-frontier-20261008/catalogue-mixture-sampling/results/exact_controls.json',
     '3452881ca5ebbd9ce22c0e25a93067966efb9ab6', '54cd8bd22eb688c1c05b84cdf2b3819166a029bcf0f291eb7078db3d595c33ed', 11956),
    ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/crossed-code-root-review/frozen/CORNER_SIGNATURE_CONTROL.json',
     'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/root-next-operations/CORNER_SIGNATURE_CONTROL.json',
     '00c82ce302c5b7d85af9d2846a6df398a65bb845', 'bc816be61d1f3fcfcead9dcc30eb9a58f3be38c8c327a6d96d4771fe30e0e430', 1358),
    ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/crossed-code-root-review/frozen/CROSSED_INTERIOR_DETERMINANT.json',
     'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/root-next-operations/CROSSED_INTERIOR_DETERMINANT.json',
     '7b190db98563735d9b254df2453c9ef27acd017f', '2d504a2e2d242e07eb5777272137b353df684ea4fa3a07169f2fcebdc44ac073', 1049),
    ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity-review/replayed_appendix_controls/results/efficiency_controls.json',
     'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity/results/efficiency_controls.json',
     '52a020ceb243df65252d2eb30a04eb2129f74ebf', '1f410340c77564bf6d9aad1a3e6af66afb04275694fadb4d379e0f32b8b0ffc2', 1152),
    ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity-review/replayed_author_controls/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity/results/exact_controls.json',
     'ca94905c40853d27de21c96d92ea33af1b8b6747', '1115ba405c6e115f15cc0b7c748a307e2335f2cb4d106cd6a03bf502aab8e596', 1173),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/global-calibration-ambiguity/MANIFEST.json',
     'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity/MANIFEST.json',
     '6d41bffbe287a5e17e7ed1a9001fa3e4a8a8c641', '819b9c5eda8de1fd35b34714d24964ce02d4a41b5c6419413bcd8d82a6febe6c', 3611),
    ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/multi-root-adaptive-review/author_replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/multi-root-adaptive-bound/results/exact_controls.json',
     'ca9cecbe23b26560841153ef24f2ea027d9cb14c', 'abcc9a3e3660314a3364da1c5262de222193ca692c538d04708a198d5e9ab6b4', 13356),
    ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/review/replay/results/NEGATIVE_CONTROLS.json',
     'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/results/NEGATIVE_CONTROLS.json',
     '3ffffeaeab27cd14f5025e21de0e8bc5298aa326', '489ea390807acce019accb27190abf7525c65241469f6496bd14ad5782c0fadf', 621),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/grouped-calibration-invariants-review/replayed_author_controls/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/grouped-calibration-invariants/results/exact_controls.json',
     '049869ebf8b1d428518448e3964244b9f1890637', '6d6a436a6f318ff39e9bc457a5bb7ebba384d559af68a855fe3a9d8b439d7c22', 2809),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/independent/INDEPENDENT_CONTROLS.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/INDEPENDENT_CONTROLS.json',
     'cdbfd3383a0496b14ee46d08cb49bbe02ee77c3c', 'c4f01971fcc1b5c31a4a36bd47642554221ba4217f38355e07bd45a2667aa353', 857),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction/results/review_verification.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/VERIFICATION.json',
     '53b1194884c22420c89aad38cd6fb9eeff0e5870', '9d7fff67839a3f665517cfb813359e64e4d91498d55df453e38f5bda315f254f', 412),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/author_replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction/results/exact_controls.json',
     'e37fa1d113849f5f5e89685ba0556ceb4b975e0c', '86b3c4bc0bba32cf1845d6768df85565404c6f197c556d79fe4935fb55d441d6', 1156),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/author/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction/results/exact_controls.json',
     'e37fa1d113849f5f5e89685ba0556ceb4b975e0c', '86b3c4bc0bba32cf1845d6768df85565404c6f197c556d79fe4935fb55d441d6', 1156),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/results/review_verification.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/FINAL_VERIFICATION.json',
     '0fdf9089c56ded8c5a48801b27529b4311c8e27c', 'b5e520b7b0edb4e8e68843e80c3d6d7760337e8283dd33753b557cf7772d6ad8', 676),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/results/exact_controls.json',
     'c650b2ed1a53b797ccf8380720426f4d322193d4', '5720a0aab8d45828c14245d89381348af73842e6a44ff7cadd9e7dc6771ebff1', 1076),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/results/exact_controls.json',
     'c650b2ed1a53b797ccf8380720426f4d322193d4', '5720a0aab8d45828c14245d89381348af73842e6a44ff7cadd9e7dc6771ebff1', 1076),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/results/exact_controls.json',
     'c650b2ed1a53b797ccf8380720426f4d322193d4', '5720a0aab8d45828c14245d89381348af73842e6a44ff7cadd9e7dc6771ebff1', 1076),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/results/panel_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/results/panel_controls.json',
     '95b534ad24631d7ae3d8add40591b286ea6c101d', '4467534cca35cd63de8f3d0bfd45cbef5cfcdd8948f779c8af41cc402c7500a7', 535),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/results/panel_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/results/panel_controls.json',
     '95b534ad24631d7ae3d8add40591b286ea6c101d', '4467534cca35cd63de8f3d0bfd45cbef5cfcdd8948f779c8af41cc402c7500a7', 535),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/results/panel_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/results/panel_controls.json',
     '95b534ad24631d7ae3d8add40591b286ea6c101d', '4467534cca35cd63de8f3d0bfd45cbef5cfcdd8948f779c8af41cc402c7500a7', 535),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/SOURCE_BINDINGS.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/SOURCE_BINDINGS.json',
     'fc8c70e78349328bc98d6318db713e832558b905', 'd295a32a9051db9540980bda48781dcd10e66a3bf9a6ec453f2f976edbe8eb17', 11953),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/stable-grouped-invariants-review/author_replay/results/GRID_WITNESS.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/stable-grouped-invariants/results/GRID_WITNESS.json',
     'dc111a35fa2e38278f17eea3fe10d3ae269b55ee', '521dc54a035408817863d03ad46ce871e47a402b5d056d25dc9916384fe03677', 2447),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/stable-grouped-invariants-review/author_replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/stable-grouped-invariants/results/exact_controls.json',
     '9b27582b15b5729a63fe7a6e4fd2df85f94b3e7c', '3a79888324acb7199f2ee2517e12a1732895da39d6d65b0fb4b143a52c04e000', 22831),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/bounded-interaction-detection/results/review_verification.json',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/bounded-interaction-detection-review/VERIFICATION.json',
     'e2fa18ef4cf9f8bfd5279e0fa5e41960e5a93313', '1f5f1448377d8ede1137eedfbdaaa09d26d66cd234b7f4ef29bfe094864ab202', 249),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/bounded-interaction-detection-review/author_replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/bounded-interaction-detection/results/exact_controls.json',
     '7e52bb4f0dd7f160f30eb3955403eca7caab2794', '74df7532deff48971dcf342ecaa5a21b0bfb4626a6b6853fceb2dd627f20bba2', 1120),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/dependent-gate-transport-review/replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/dependent-gate-transport/results/exact_controls.json',
     '82b17f1be444762f878b42d51bd80de8e18afca8', 'cb68c4936ac039a7046a411d717078e1212006fbabb0fd8620ef98bf679779db', 18639),
    ('research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/dependent-gate-transport/SOURCE_BINDINGS.json',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/dependent-gate-transport/SOURCE_BINDINGS.json',
     'b672e95b7f86cc8d5f3c78353e1041bbe5e2608e', 'd0168bae91d619e795e50326caaf91e6a19df0e5cb84f8b1e1562a53646c5c0a', 6234),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/dependent-gate-transport/results/final_review_verification.json',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/same-threshold-replay/results/predecessor_verification.json',
     '8d804c7a822234df208caa44f61835c70cdd3b59', 'bebb17eace4e5bed8431fa6d8daed38d92c53ec568c7557cf22b2eac60e1c817', 556),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/finite-hypergraph-calibration-review/packaging_addendum/author_replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/finite-hypergraph-calibration/results/exact_controls.json',
     'a7ff78d1b08b12d9a1116cf6ef8a66b0017f1d02', 'e5b43da0d25414ed320013046f4186f7e7b14c1e511f65b9a94ea3564557e8b4', 2125),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/finite-hypergraph-calibration-review/packaging_addendum/author_snapshot/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/finite-hypergraph-calibration/results/exact_controls.json',
     'a7ff78d1b08b12d9a1116cf6ef8a66b0017f1d02', 'e5b43da0d25414ed320013046f4186f7e7b14c1e511f65b9a94ea3564557e8b4', 2125),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/finite-hypergraph-calibration-review/packaging_addendum/author_snapshot/SOURCE_BINDINGS.json',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/finite-hypergraph-calibration/SOURCE_BINDINGS.json',
     'e3b50fec923b60d8d834d0940fa43765135ade04', '2c1facf6e9e5cd35a4cdc3bc3e522f5a9a510b85b8e4f7a8f4a379fdcbaa750e', 5010),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/same-threshold-replay-review/replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/same-threshold-replay/results/exact_controls.json',
     '9eed1cbf88853aafd60ab5ac7f1ef5e1a3f2bf04', '060ed3aae850901e96d00a59b2b42f10e7c3e933628cd97e7503b8368b656596', 3717),
    ('research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/same-threshold-replay/SOURCE_BINDINGS.json',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/same-threshold-replay/SOURCE_BINDINGS.json',
     '36381587fa5fadb645f0fc3fc0e630f8d74d9287', 'adfbc884c980593876b941e3b8c7327ac5294623a0e5d4463001aa556d5e7a7c', 7996),
    ('research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/arbitrary-face-replay-design-final-review/AUTHOR_CONTROLS_STRENGTHENED_RERUN.json',
     'research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/arbitrary-face-replay-design/CONTROLS_OUTPUT.json',
     '78e0d13f8dcce7f7d3343332e5a72a0a39ec7a95', '9af0caefa09b181bb9d3141836a8b21d3a40ac4e4f41734b3d5184bfe180e209', 3417),
    ('research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/arbitrary-face-replay-design-final-review/REVIEW_RECEIPT.json',
     'research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/arbitrary-face-replay-design-final-review/REVIEW_RECEIPT.json',
     '3ae4653929b83f93853c40bf7377143412f3623a', 'f6932faa5f49ffbe6b11826eeb4e25de79a3bc196203ccf8e2c9ebf1785f5f34', 6949),
    ('research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/arbitrary-face-replay-design-final-review/SOURCE_BINDING_RERUN.json',
     'research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/arbitrary-face-replay-design/SOURCE_CHECK_OUTPUT.json',
     'af883751854a8c24805119ca40c9f7eb7ffea779', '11ba8909fdfbac2214f9a0252341431d6165ca9be4a4c504952f8f2c8d023cbf', 6393),
    ('research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/arbitrary-face-replay-design/MANIFEST.json',
     'research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/arbitrary-face-replay-design/MANIFEST.json',
     '9c10ee19195f460e96a0a8e8655d00ae03b6a5f9', 'e454504588064ed84b4565fbc4656075c456a34b3f812973f1c96c5d4d83af3f', 2503),
    ('research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/finite-replay-sampling-lower-bound/results/final_review_verification.json',
     'research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/finite-replay-sampling-lower-bound-review/FINAL_VERIFICATION.json',
     'b3ee5d543c199d184afbe0b40ee554e42cd992f7', '69a7bae07a7de7751ab9ac7199e379acf66a3023b96ba08147d2d8de83eac0c3', 4556),
    ('research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/finite-replay-sampling-lower-bound-review/author_snapshot/MANIFEST.json',
     'research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/finite-replay-sampling-lower-bound/MANIFEST.json',
     'e554982ab2e0b4149b420c6662335e84693a084b', '3f7db7a3045f45135af93f82130791635cb56c808caf9aae89d137966095fa23', 1664),
    ('research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/finite-replay-sampling-lower-bound-review/author_snapshot/SOURCE_BINDINGS.json',
     'research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/finite-replay-sampling-lower-bound/SOURCE_BINDINGS.json',
     'c355d37cfa9b2749089df9e24b26fffdedc325a8', 'f642a4a2214d76d50edfbaad21d8356a02e0f723ac8db304d92dd205abd6375a', 9703),
    ('research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/finite-replay-sampling-lower-bound-review/author_snapshot/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/finite-replay-sampling-lower-bound/results/exact_controls.json',
     'fc54186c5c1b9e6d93b8a09550d1aa7e9126b4c8', '3eadf7e16d2c499d9b405f3186a4ccee9072ab34e4b6f0b3776bcc4bb0037ac2', 25985),
    ('research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/adaptive-two-face-corollary-review/AUTHOR_CONTROLS_RERUN.json',
     'research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/adaptive-two-face-corollary/CONTROLS_OUTPUT.json',
     'e94c7aa821a0cf4a6b3662c6e8a39beea5a161d1', 'f8d4044b165117ecdacc79cbb5b2bea8326f17e30fcf8dac16ce5731508612aa', 1466),
    ('research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport-review/INDEPENDENT_PROBE_RESULTS.json',
     'research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport-review/INDEPENDENT_RUN_OUTPUT.json',
     'bc1526e355a6b1c068b6253ba4416b36d5cadcaa', '327b28c4e2847191c37c46d25c1687edd448dcd8a6df6d0170f4aa2d0c786509', 1590),
    ('research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport-review/REPLAY_RUN_OUTPUT.json',
     'research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport/RUN_OUTPUT.json',
     '1730b8a3ce4d9270dd811b8ea1c9745c7d7ef742', '8b2328daae9ff60292316e651f07f34382b399ac002673e59e165d6eee226a7e', 2934),
    ('research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport-review/reviewed_snapshot/CONTROL_RESULTS.json',
     'research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport/RUN_OUTPUT.json',
     '1730b8a3ce4d9270dd811b8ea1c9745c7d7ef742', '8b2328daae9ff60292316e651f07f34382b399ac002673e59e165d6eee226a7e', 2934),
    ('research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport-review/reviewed_snapshot/RUN_OUTPUT.json',
     'research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport/RUN_OUTPUT.json',
     '1730b8a3ce4d9270dd811b8ea1c9745c7d7ef742', '8b2328daae9ff60292316e651f07f34382b399ac002673e59e165d6eee226a7e', 2934),
    ('research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport/CONTROL_RESULTS.json',
     'research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport/RUN_OUTPUT.json',
     '1730b8a3ce4d9270dd811b8ea1c9745c7d7ef742', '8b2328daae9ff60292316e651f07f34382b399ac002673e59e165d6eee226a7e', 2934),
    ('research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/full-face-threshold-kl-review/CONTROL_RESULTS.json',
     'research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/full-face-threshold-kl-review/checks.stdout.json',
     'b7d50e8f8b35f2912347f47e76ca066ce103942f', 'c501ee9cbc1019f4d89c15d36d2a27fa24465ae16be0b84e03deaf7052a2aab8', 6894),
    ('research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate-review/AUTHOR_CONTROL_RESULTS.json',
     'research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate/CONTROL_RESULTS.json',
     '4d85a649faae154ccf545eebfd9ce1ea2b502e25', 'a3e4120b7146789bf5f076c1a3fe1ec6d98752a1719fcc9b7f5ab36bbc62c97f', 2459),
    ('research/t20-live-20261009/checkpoints/CP10/t20-next-frontier-20261008/retained-skyline-likelihood/CONTROL_RESULTS.json',
     'research/t20-live-20261009/checkpoints/CP10/t20-next-frontier-20261008/retained-skyline-likelihood/check_stdout.json',
     '28a07bddc742bcbd9829be94a0b18864ae412204', '9d593577eda951f90327228cdc079ef22c0a776206c5063350e8cfcc686255df', 6899),
    ('research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/baseline-skyline-moments-review/source-rerun/CONTROL_RESULTS.json',
     'research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/baseline-skyline-moments/CONTROL_RESULTS.json',
     '18a13c923a3036aabd93a3f7b6c4da8373cbbfca', '83094e37c1749ed43c2363eba0d8914f18b946558e15cba0ddfbe211859abc41', 19923),
    ('research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/full-skyline-log-squared-review/author_replay/CONTROL_RESULTS.json',
     'research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/full-skyline-log-squared/CONTROL_RESULTS.json',
     '9ac1c9e6794ec548dc89e2c8e707ee886bd8effb', '6de20900a23a8578bfe57dfab63f2147c517c5a8cd606a74ff02b4646c3a5211', 52456),
    ('research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/full-skyline-reverse-kl-review/author_replay/CONTROL_RESULTS.json',
     'research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/full-skyline-reverse-kl/CONTROL_RESULTS.json',
     '073296a01b255a9c1d670571222b791fe43d820d', '68e99ec9eb962d4922ccd6b3a9cad981c770d0edd461e83dbaace1c3d0802ddc', 11873),
    ('research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/skyline-likelihood-score-review/author_replay/CONTROL_RESULTS.json',
     'research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/skyline-likelihood-score/CONTROL_RESULTS.json',
     'd9c5d2355a9a036c5d7961ddd6de5907da008aec', 'fc4e65e6f42844a9c886881a60b95fcccefa8a10defe48a26d733f31ad8cdab9', 10323),
    ('research/t20-live-20261009/checkpoints/CP12/t20-next-frontier-20261008/finite-geometric-score-review/author_replay/CONTROL_RESULTS.json',
     'research/t20-live-20261009/checkpoints/CP12/t20-next-frontier-20261008/finite-geometric-score/CONTROL_RESULTS.json',
     'b8a6d1ddc6371a90dee82c725d11b30d331622ba', 'c799b4ef7dafaa5daba4f7c81c22372a68ce33f2dc49d3453f383087c029faf6', 6659),
    ('research/t20-live-20261009/checkpoints/CP12/t20-next-frontier-20261008/sharp-skyline-information-review/author_replay/CONTROL_RESULTS.json',
     'research/t20-live-20261009/checkpoints/CP12/t20-next-frontier-20261008/sharp-skyline-information/CONTROL_RESULTS.json',
     '673208ce24f8a47e474c17d95c9f050a98cb08cb', 'bbcce6cec92d9009bf9fcfa79f66bc3c7135e3fb231a3202c4eff2cde4197d04', 9891),
    ('research/t20-live-20261009/checkpoints/CP12/t20-next-frontier-20261008/sharp-skyline-information-review/author_replay_pre_freeze/CONTROL_RESULTS.json',
     'research/t20-live-20261009/checkpoints/CP12/t20-next-frontier-20261008/sharp-skyline-information/CONTROL_RESULTS.json',
     '673208ce24f8a47e474c17d95c9f050a98cb08cb', 'bbcce6cec92d9009bf9fcfa79f66bc3c7135e3fb231a3202c4eff2cde4197d04', 9891),
    ('research/t20-live-20261009/checkpoints/CP13/t20-next-frontier-20261008/modal-grounding-source-review/input-snapshot/MANIFEST.json',
     'research/t20-live-20261009/checkpoints/CP13/t20-next-frontier-20261008/modal-grounding-source/MANIFEST.json',
     '7bae2d8c9d92c318654f8e264f15f5c9f2595592', '94756f946b2e9c0aca406de2bed11471fb62f40fbbd939a9faeea590ea11c6a0', 3874),
    ('research/t20-live-20261009/checkpoints/CP13/t20-next-frontier-20261008/modal-grounding-source-review/input-snapshot/READING_LEDGER.json',
     'research/t20-live-20261009/checkpoints/CP13/t20-next-frontier-20261008/modal-grounding-source/READING_LEDGER.json',
     '02c3d956bf363702185c02162281aeb426a2c5c8', '02520251152c138d53157583461112a0613f9ba8893917a2b1ee52cbdf8f0e9e', 7167),
    ('research/t20-live-20261009/checkpoints/CP13/t20-next-frontier-20261008/modal-grounding-source-review/input-snapshot/SOURCE_EXTRACTION_CHECK.json',
     'research/t20-live-20261009/checkpoints/CP13/t20-next-frontier-20261008/modal-grounding-source/SOURCE_EXTRACTION_CHECK.json',
     '4f407fadee5f03d5fb32a0f20c35738759fcf356', '749121d3e535ade49a942db72b54b8797d6856dcac85bf9982f676b0a18e7295', 11785),
    ('research/t20-live-20261009/checkpoints/CP13/t20-next-frontier-20261008/modal-identity-transport-review/AUTHOR_REPLAY.json',
     'research/t20-live-20261009/checkpoints/CP13/t20-next-frontier-20261008/modal-identity-transport/CONTROL_RESULTS.json',
     'c8841f04eeacee47b36fb5a1a393aa3c9a860948', 'f740b49863794c4319a508f152a30c17270a96b4ec58925ff57a0ea5da40a676', 2531),
    ('research/t20-live-20261009/checkpoints/CP13/t20-next-frontier-20261008/modal-identity-transport-review/INDEPENDENT_RUN.stdout.json',
     'research/t20-live-20261009/checkpoints/CP13/t20-next-frontier-20261008/modal-identity-transport-review/INDEPENDENT_RESULTS.json',
     '0dab1dbe0f299ff87e5b5a9de5f673a6de1727f8', '124bdd9bd4923a9e6f6cc72e73849a77a1d24a7c47f391bb824011d6d784181a', 2541),
    ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/compilation-replay/CHECK_RESULTS.json',
     'research/t20-live-20261009/checkpoints/CP23/certificate-compilation-boundary-20261009/CHECK_RESULTS.json',
     'fe26c132e95bf846f430684ad47c5ef25fbd6117', 'b61b2037c1c51e740d62bfff9f1fbf163beeaf8cedf4a2a50d273c108e632193', 693),
    ('research/t20-live-20261009/checkpoints/CP23/certificate-compilation-boundary-20261009/review/parent-sanity-replay.json',
     'research/t20-live-20261009/checkpoints/CP23/certificate-compilation-boundary-20261009/review/SANITY_RESULTS.json',
     'a4897484b5e22af8cabc21e27ed4f045ab014e62', '99c3b0d71e34d8e0c14293d82af499cdacd77fffd2089070603167079aa45c8d', 419),
    ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/discrimination-replay/CHECK_RESULTS.json',
     'research/t20-live-20261009/supplement/S01/warranted-discrimination-research-20261009/CHECK_RESULTS.json',
     '3a72114f350daf55cd10f27de132be3456fcf327', '429fc2e93da069d5ac61b7527860f74ecb83e73e9d780e6caf85a51b9e60a602', 813),
    ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-research-20261009/CHECK_RESULTS.json',
     'research/t20-live-20261009/supplement/S01/warranted-discrimination-research-20261009/CHECK_RESULTS.json',
     '3a72114f350daf55cd10f27de132be3456fcf327', '429fc2e93da069d5ac61b7527860f74ecb83e73e9d780e6caf85a51b9e60a602', 813),
    ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/BINDING.json',
     'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/BINDING.json',
     '3b1fae41d0ae0f62c081c14329dc1348e85a4ab3', '4641da2105a959860230f681a1813d935b36f05886197479f4b520de63175053', 4685),
    ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/CHECK_RESULTS.json',
     'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/CHECK_RESULTS.json',
     '483b7c4a04b4c5891293de42f47e006a19a03c2f', '8b9f27b9a7274f3c5cba2b95458694e48989a72aa2b899048148762ea52ca0d5', 714),
    ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/MANIFEST.json',
     'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/MANIFEST.json',
     'c1fb9b0fa36e286d68cd397ce051ded6023d651b', '5e07ae5129e8191288c901a919f54821ba5123636110655e23f2114dc5d2a58a', 6735),
    ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-research-20261009/MANIFEST.json',
     'research/t20-live-20261009/supplement/S01/warranted-discrimination-research-20261009/MANIFEST.json',
     '93f23708fafd1cf214a60b4d06c4b71e86fdc0fd', 'a09fda18d1dd4e524d18278447ca3dfef267561a89e466e0f82b8dcfd5a77c31', 2313),
    ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-research-20261009/SOURCES.json',
     'research/t20-live-20261009/supplement/S01/warranted-discrimination-research-20261009/SOURCES.json',
     '317bde77327463310dfdd08bf4a4cab95011f477', '188bbf65c49669cae64022a810f5a35b4b846cd0a91497865e62811edda82b25', 4350),
)
CHECKPOINT_RECORD_COPY_CATALOG_SHA256 = 'b7d996ff4bbbbeb8000d9bd1d87449fd760b5a7a3a0563f328dbcd24da0ca85c'
CHECKPOINT_RECORD_COPY_PATHS = frozenset(row[0] for row in CHECKPOINT_RECORD_COPY_MEMBERS)


# Exactly12 previous checkpoint providers now have an exact surviving body.
# The original87 catalog stays intact. Both the prior coordinate and final
# provider must authenticate; a corrupt present or staged intermediate fails.
CHECKPOINT_COPY_RETARGETS = (
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction-review/author_replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/author_replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction/results/exact_controls.json',
     'e37fa1d113849f5f5e89685ba0556ceb4b975e0c', '86b3c4bc0bba32cf1845d6768df85565404c6f197c556d79fe4935fb55d441d6', 1156),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/author/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/author/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction/results/exact_controls.json',
     'e37fa1d113849f5f5e89685ba0556ceb4b975e0c', '86b3c4bc0bba32cf1845d6768df85565404c6f197c556d79fe4935fb55d441d6', 1156),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/independent/INDEPENDENT_CONTROLS.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/independent/INDEPENDENT_CONTROLS.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/INDEPENDENT_CONTROLS.json',
     'cdbfd3383a0496b14ee46d08cb49bbe02ee77c3c', 'c4f01971fcc1b5c31a4a36bd47642554221ba4217f38355e07bd45a2667aa353', 857),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction/results/review_verification.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction/results/review_verification.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/VERIFICATION.json',
     '53b1194884c22420c89aad38cd6fb9eeff0e5870', '9d7fff67839a3f665517cfb813359e64e4d91498d55df453e38f5bda315f254f', 412),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/results/exact_controls.json',
     'c650b2ed1a53b797ccf8380720426f4d322193d4', '5720a0aab8d45828c14245d89381348af73842e6a44ff7cadd9e7dc6771ebff1', 1076),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/results/panel_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/results/panel_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/results/panel_controls.json',
     '95b534ad24631d7ae3d8add40591b286ea6c101d', '4467534cca35cd63de8f3d0bfd45cbef5cfcdd8948f779c8af41cc402c7500a7', 535),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/SOURCE_BINDINGS.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/SOURCE_BINDINGS.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/SOURCE_BINDINGS.json',
     'fc8c70e78349328bc98d6318db713e832558b905', 'd295a32a9051db9540980bda48781dcd10e66a3bf9a6ec453f2f976edbe8eb17', 11953),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/results/exact_controls.json',
     'c650b2ed1a53b797ccf8380720426f4d322193d4', '5720a0aab8d45828c14245d89381348af73842e6a44ff7cadd9e7dc6771ebff1', 1076),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/results/panel_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/results/panel_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/results/panel_controls.json',
     '95b534ad24631d7ae3d8add40591b286ea6c101d', '4467534cca35cd63de8f3d0bfd45cbef5cfcdd8948f779c8af41cc402c7500a7', 535),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/results/exact_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/results/exact_controls.json',
     'c650b2ed1a53b797ccf8380720426f4d322193d4', '5720a0aab8d45828c14245d89381348af73842e6a44ff7cadd9e7dc6771ebff1', 1076),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/results/panel_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/results/panel_controls.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/results/panel_controls.json',
     '95b534ad24631d7ae3d8add40591b286ea6c101d', '4467534cca35cd63de8f3d0bfd45cbef5cfcdd8948f779c8af41cc402c7500a7', 535),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor/results/review_verification.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/results/review_verification.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/FINAL_VERIFICATION.json',
     '0fdf9089c56ded8c5a48801b27529b4311c8e27c', 'b5e520b7b0edb4e8e68843e80c3d6d7760337e8283dd33753b557cf7772d6ad8', 676),
)
CHECKPOINT_COPY_RETARGETS_SHA256 = '275cdaf159464f7a2dfbff36766742c7944c277cc1fe721e8200e61ebb740eee'


# Exactly52 redundant archived Python source coordinates. The bytes remain
# inert evidence with their original date, role and context; this route does
# not execute old programs, preserve a current historical CLI or permit removal.
CHECKPOINT_CODE_COPY_MEMBERS = (
    ('research/t20-live-20261009/checkpoints/CP01/recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-frontier-continuation/sovereignty-choice-semantics/reactive-context-extension/src/reactive_context.py',
     'research/t20-live-20261009/checkpoints/CP01/recovery-t20/addendum/tranche20/research-frontier-continuation/sovereignty-choice-semantics/reactive-context-extension/src/reactive_context.py',
     '14f8836f0c8b8a7e64a7943db200311204d8a88d', 'f73cee9c0271dd2a80843a3994534e1119fca33386e59a483f3175d69880a6cc', 6736),
    ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/productive-identifiability/general-roots/src/design_rank.py',
     'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/identification-review/frozen-general-v1/design_rank.py',
     '24ec8da899ff548dcbadab483dc32a58962bf456', '37cf8f723bf3813ea2fecbe04185297eae30b4d2de8618f83715329bc8c9284a', 5995),
    ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/productive-identifiability/general-roots/src/test_design_rank.py',
     'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/identification-review/frozen-general-v1/test_design_rank.py',
     '5356c8213a11acb840f284d2b79b4cb4d388d114', '5ec96690318ecbbe3f56a7bf1f0bda07468113d7c50329f6c2ef7b9c66929df2', 3761),
    ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/identification-review/frozen-v2/identifiability.py',
     'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/productive-identifiability/src/identifiability.py',
     'd3a3fb5d457e047adb67e29d495d9955f698d569', 'c35e212dbc24066ec3f1baf6e4fe753d5eb16e71b1318f5d307de6c805d33c3d', 7578),
    ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/identification-review/frozen-v2/test_identifiability.py',
     'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/productive-identifiability/src/test_identifiability.py',
     '2a4342179eff5e23b74ad91dec169152e48dab5c', 'd55a1d852bda9a90e0980329b60f60206447c132bbb94b4f5a1891b71ed744ff', 11889),
    ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/single-calibration-review/frozen/crt_calibration.py',
     'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/single-calibration-design/src/crt_calibration.py',
     '894119aece108e7fc93e6edd979e59edbcd44198', '8aa9f0b05291efdd876e9e9c2e4f04eeb09959b7b3d96adb1d6a4ee149faecec', 5074),
    ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/single-calibration-review/frozen/test_crt_calibration.py',
     'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/single-calibration-design/src/test_crt_calibration.py',
     '1efb6d326805c1afe2a11607e6b6cc1cba5c0692', '76cf268e728af85faea8ab56ae36525dba04ace25e24de08f596f5a78a61924c', 5692),
    ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/countable_support.py',
     'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/countable_support.py',
     '0d09017120146576d7d58d6760747efff05a7712', 'e6e928ce4894770b671e1b74b4c7cf2f88e5a3b767bdbd28c0dd03a6b923e2f6', 8119),
    ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/gcd_decoder.py',
     'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/gcd_decoder.py',
     '8ec47140335456b7cb1bced055f80aa86f22ba92', '3450a5cf943da435984a48bbb8e04a5c4cdb13ad7fa89bed48f18738ba70d827', 4257),
    ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/oracle_boundaries.py',
     'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/oracle_boundaries.py',
     '041fb80e6a60a25ddef3eaf67260661737fee6cf', 'f39ed4839663137b7c7863211de97fd6c33cf5b75486b5f96fd02cbc181cc060', 4206),
    ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/test_countable_support.py',
     'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/test_countable_support.py',
     '4c983e003732e859f699e22e1f78175e04fc5dc9', '52aca0366e185b21c8f61437dd3c79ab3935f38bbe64246c9215870d9890ceed', 7560),
    ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/test_gcd_decoder.py',
     'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/test_gcd_decoder.py',
     '77a0708d3164f71e25f1167aea856bf3ec300850', 'ce0ad237e36bfdb16f5b52a90e387d750bf91a7e5f5001c78178612d9910e676', 2502),
    ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/test_oracle_boundaries.py',
     'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/test_oracle_boundaries.py',
     'f8fe51c5d92d77d7361830a5b6e54e7e3344e161', 'e03e1a5721aec610e0cc88c7a372cb37292cfdd8f8aa5bcb71a31f7bd91df8ba', 3857),
    ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/grouped-mixture-identification/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/grouped-mixture-review/frozen/exact_controls.py',
     '465b4c947f0f25b357a4f85f48daf79ce27ef71b', '7b9dbb1f7fa25a7165c421f61b3b2fd257a8c4f2a9d4446efde822900107cf82', 9072),
    ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/noise-aware-calibration/src/robust_masks.py',
     'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/noise-aware-review/frozen/robust_masks.py',
     '8431f617edbe9d2429c9f3705bd26c1525c67bce', '1c818590a66e5e6b7af39d46c2db849bb2bb99e758a90771218c4b2cb148efd3', 9511),
    ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/noise-aware-calibration/src/test_robust_masks.py',
     'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/noise-aware-review/frozen/test_robust_masks.py',
     '4422a35f856298cfc5537fd5d39dd597c51cd7ab', 'e9e1a14061d66a77fac35659d80b7f7298294afb940cdc797b5db62fee3d46c2', 6722),
    ('research/t20-live-20261009/checkpoints/CP03/t20-next-frontier-20261008/catalogue-mixture-review/frozen/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP03/t20-next-frontier-20261008/catalogue-mixture-sampling/exact_controls.py',
     '9433cc2df1ec94ab353b5a19405945ba1ed70ff7', '9e92b5affb6ce926bca92e39a9e222b051cdc47bd8f1efd6d78a98d2c0752d77', 8504),
    ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity-review/replayed_appendix_controls/efficiency_controls.py',
     'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity/efficiency_controls.py',
     'd775415f97b3af7f65ba7fad639d1fe8fac453aa', '968268172209211e9c7dff218cc3a9acc97f6f765aac53d8569992dd1a239a6f', 4643),
    ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity-review/replayed_author_controls/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity/exact_controls.py',
     'fa7568bc43686b4408803c75b5b844b00944a5ee', '867de73098d4eb210ef4fbbf5758c728efeb4dbe46982bd80941630fed00a2d2', 4912),
    ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/multi-root-adaptive-review/author_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/multi-root-adaptive-bound/exact_controls.py',
     '39c071038918ecff66460a2d318664f51cd4071c', 'c503cdaf9391b69dc503510ef05ff656c85aa6989f33ded6e75397cef1679907', 6327),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/grouped-calibration-invariants-review/replayed_author_controls/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/grouped-calibration-invariants/exact_controls.py',
     'd283498dafd14ea38d2c926f453b7971130cc61d', 'aa8c7c45fc8f2f803aaf4535a6eec6f49b67048e59d0ab8ca402b4fb77ca1af1', 7255),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/author_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction/exact_controls.py',
     '4f78222a0ab2d0e4cb4972cb62e110436cc817ed', '92cd73364482270d5acb49190a4f5eb893c4f646aa052281fb2fdbe21c1c2b70', 5030),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/author/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction/exact_controls.py',
     '4f78222a0ab2d0e4cb4972cb62e110436cc817ed', '92cd73364482270d5acb49190a4f5eb893c4f646aa052281fb2fdbe21c1c2b70', 5030),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/independent/independent_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/independent_controls.py',
     'a261bcd23a0263de2df88b14016a58984c234f8a', 'ed2d1faf38772231440c05dc440068abe4849f5a5474a21d890bf6d0502aa1ba', 6836),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/exact_controls.py',
     '4bcf6cd4a98548c23e03a82987bf6ccfad57f1a9', '9ac147575d35266debd88dfd23d91cb2f96cded9823ac85c0e5a109275eea11c', 4780),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/exact_controls.py',
     '4bcf6cd4a98548c23e03a82987bf6ccfad57f1a9', '9ac147575d35266debd88dfd23d91cb2f96cded9823ac85c0e5a109275eea11c', 4780),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/exact_controls.py',
     '4bcf6cd4a98548c23e03a82987bf6ccfad57f1a9', '9ac147575d35266debd88dfd23d91cb2f96cded9823ac85c0e5a109275eea11c', 4780),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/panel_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/panel_controls.py',
     'a5b7dfe4518398e7d2cf88ee71b70cc904290365', '0503ae9f04d0b484df886c9123d004ec18953d09c2487b47c91fdf16b2e7435b', 2826),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/panel_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/panel_controls.py',
     'a5b7dfe4518398e7d2cf88ee71b70cc904290365', '0503ae9f04d0b484df886c9123d004ec18953d09c2487b47c91fdf16b2e7435b', 2826),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/panel_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/panel_controls.py',
     'a5b7dfe4518398e7d2cf88ee71b70cc904290365', '0503ae9f04d0b484df886c9123d004ec18953d09c2487b47c91fdf16b2e7435b', 2826),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/verify_evidence.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/verify_evidence.py',
     '9c92a346d92a803c528220689b02bdbdd212bd10', '8f41b467eb27f7dea863074e5886f477d0cc02f613a82dbea6e45a4a3d007093', 2252),
    ('research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/stable-grouped-invariants-review/author_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/stable-grouped-invariants/exact_controls.py',
     'c3c1418cc6d3d639cb55c1b65b7c5c29f5a0999e', 'bb247d16c51a1427fa13226c396bedc3fbab02d1062e353382deabee587c57b9', 9541),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/bounded-interaction-detection-review/author_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/bounded-interaction-detection/exact_controls.py',
     '7fb03d67af2f6b8e0e189ea4ea732b1347549830', '6c4859846a169b94ba75e4a8087cfc432dc511d76a993a9f2e8f5e597e5e5a45', 7535),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/dependent-gate-transport-review/replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/dependent-gate-transport/exact_controls.py',
     '39381d893a2be45a8dc32255c6fd3db9b3470c2e', 'c67207bacb7b38bb939ae6bd5d60bda44f63d489aa495c588f973c6b9cf9ffd1', 6916),
    ('research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/dependent-gate-transport/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/dependent-gate-transport/exact_controls.py',
     '39381d893a2be45a8dc32255c6fd3db9b3470c2e', 'c67207bacb7b38bb939ae6bd5d60bda44f63d489aa495c588f973c6b9cf9ffd1', 6916),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/finite-hypergraph-calibration-review/packaging_addendum/author_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/finite-hypergraph-calibration/exact_controls.py',
     '987adb4db1d177cc52e02a2d13dcd0f3708969a4', '30d362bfc64e01e53b3e9a8be9ffe4a3432b6d074beed27872894c550d3f6bee', 9581),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/finite-hypergraph-calibration-review/packaging_addendum/author_snapshot/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/finite-hypergraph-calibration/exact_controls.py',
     '987adb4db1d177cc52e02a2d13dcd0f3708969a4', '30d362bfc64e01e53b3e9a8be9ffe4a3432b6d074beed27872894c550d3f6bee', 9581),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/same-threshold-replay-review/replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/same-threshold-replay/exact_controls.py',
     'afbda6f9783e11ea3149a89273cce6bf6576a8d5', '0e43b8b3d5dc15929e79dae69e90ea8f06091477a181f5e1a64d503a24e947b6', 7158),
    ('research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/same-threshold-replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/same-threshold-replay/exact_controls.py',
     'afbda6f9783e11ea3149a89273cce6bf6576a8d5', '0e43b8b3d5dc15929e79dae69e90ea8f06091477a181f5e1a64d503a24e947b6', 7158),
    ('research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/finite-replay-sampling-lower-bound-review/author_snapshot/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/finite-replay-sampling-lower-bound/exact_controls.py',
     '2859a5a4e467afb6bf3815a3528a02d1e1e1b75d', '2acf221085fc8f0263041e7adbf129e828e4c93a877a5ee0668729bcf6b84901', 6905),
    ('research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport-review/reviewed_snapshot/controls.py',
     'research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport/controls.py',
     'e455bbc9d1838dfb9f2467c785b010ba784a4a67', '9f1890d70aba5d3f4ca953809a588471226f3e56bb46feaf7cb82c3cf0aa3bd2', 13819),
    ('research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate-review/AUTHOR_CONTROLS_REPLAY.py',
     'research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate/controls.py',
     'cb5f6d17a425b19cebb8aa7c0050d1f9bf56e160', '8b88ebefafedf4afdee817f73420870648b5b162ffb0ad8e6699b4a2aab9dced', 5579),
    ('research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/baseline-skyline-moments-review/source-rerun/controls.py',
     'research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/baseline-skyline-moments/controls.py',
     '17da9c4757d030e1fced4d87a45e5496910c3ba4', '3f65d6f86cda2dccb9c64705a12b238d95ae04205e2508e6266ed47c8edc4fbb', 6042),
    ('research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/full-skyline-log-squared-review/author_replay/controls.py',
     'research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/full-skyline-log-squared/controls.py',
     'd45cd3c56ac118aacb1aa24fdcda502bb74022ef', '43b2eb32343777d5094c2564f4641d99fcd6354bfab3a130b9dd8d92e3c6ca8c', 8352),
    ('research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/full-skyline-reverse-kl-review/author_replay/controls.py',
     'research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/full-skyline-reverse-kl/controls.py',
     '7ec50a20fa03e42013dbb550077e01061186b7d7', 'a56ff98a0dfa7e8dbedda9b257ccfef48297eca553d2588092f86e659c4102d9', 8125),
    ('research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/skyline-likelihood-score-review/author_replay/controls.py',
     'research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/skyline-likelihood-score/controls.py',
     '57b320b02bfd8227ec43fa9f4fec80815f86c9b5', 'b1399fda7487fa985f66e5cfa6650d7a63c10b91f3d9da665c6285dcd1bd8cc5', 2333),
    ('research/t20-live-20261009/checkpoints/CP12/t20-next-frontier-20261008/sharp-skyline-information-review/author_replay/controls.py',
     'research/t20-live-20261009/checkpoints/CP12/t20-next-frontier-20261008/sharp-skyline-information/controls.py',
     '429ab66b4ac2f6907b98fa3a681de2aa358c0d60', '04e771ffc1d30e736776bc30b8d6922f36fe25867ddda05c7bc5e3289db86eb4', 9867),
    ('research/t20-live-20261009/checkpoints/CP13/t20-next-frontier-20261008/modal-identity-transport-review/author_controls_snapshot.py',
     'research/t20-live-20261009/checkpoints/CP13/t20-next-frontier-20261008/modal-identity-transport/controls.py',
     'e1e1ed0f7bae9fec968192284a04a0e0984f11e8', '12ee27b036ed5b4d5fc51b6d10bb6f937da53ec4e5186e1e98f74889af8b3d9c', 14363),
    ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/compilation-replay/compiler.py',
     'research/t20-live-20261009/checkpoints/CP23/certificate-compilation-boundary-20261009/compiler.py',
     '694261f36e31caf66ec6c2e79c1bf501e45d778c', '5da2762fe31720e898165751bf53636f66a5267719e0b3687587628c48ac4714', 6557),
    ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/compilation-replay/verify.py',
     'research/t20-live-20261009/checkpoints/CP23/certificate-compilation-boundary-20261009/verify.py',
     'd8c2bd9d095b83b557982f27620bc4a830bedb13', 'ba6b947c758b0541ce4dc489c116c87cc6000ebc221ff23f8b5f3efd5de94f70', 10995),
    ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/discrimination-replay/verify.py',
     'research/t20-live-20261009/supplement/S01/warranted-discrimination-research-20261009/verify.py',
     '6fbc0cecc3001da2aaf38e785998242786c2221a', 'bdd29fd57418db2327983bf2cb7e4c40632c9140637ae6df5d0d990ff28481b2', 7876),
    ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-research-20261009/verify.py',
     'research/t20-live-20261009/supplement/S01/warranted-discrimination-research-20261009/verify.py',
     '6fbc0cecc3001da2aaf38e785998242786c2221a', 'bdd29fd57418db2327983bf2cb7e4c40632c9140637ae6df5d0d990ff28481b2', 7876),
)
CHECKPOINT_CODE_COPY_CATALOG_SHA256 = '6ff3c4f465ee492585502ae9db8ffe53aa806cc03333f9b4219d34ea2231949c'
CHECKPOINT_CODE_COPY_PATHS = frozenset(row[0] for row in CHECKPOINT_CODE_COPY_MEMBERS)
CHECKPOINT_CODE_PUBLIC_MEMBERS = (
    'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/identification-review/frozen-v2/identifiability.py',
    'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/identification-review/frozen-v2/test_identifiability.py',
    'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/countable_support.py',
    'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/gcd_decoder.py',
    'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/oracle_boundaries.py',
    'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/test_countable_support.py',
    'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/test_gcd_decoder.py',
    'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/test_oracle_boundaries.py',
    'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/grouped-mixture-identification/exact_controls.py',
    'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/noise-aware-calibration/src/robust_masks.py',
    'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/noise-aware-calibration/src/test_robust_masks.py',
    'research/t20-live-20261009/checkpoints/CP03/t20-next-frontier-20261008/catalogue-mixture-review/frozen/exact_controls.py',
    'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity-review/replayed_appendix_controls/efficiency_controls.py',
    'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity-review/replayed_author_controls/exact_controls.py',
    'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/grouped-calibration-invariants-review/replayed_author_controls/exact_controls.py',
    'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/author_replay/exact_controls.py',
    'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/exact_controls.py',
    'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/panel_controls.py',
    'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/verify_evidence.py',
    'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/stable-grouped-invariants-review/author_replay/exact_controls.py',
    'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/bounded-interaction-detection-review/author_replay/exact_controls.py',
    'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/dependent-gate-transport-review/replay/exact_controls.py',
    'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/finite-hypergraph-calibration-review/packaging_addendum/author_replay/exact_controls.py',
    'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/same-threshold-replay-review/replay/exact_controls.py',
    'research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/finite-replay-sampling-lower-bound-review/author_snapshot/exact_controls.py',
    'research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport-review/reviewed_snapshot/controls.py',
    'research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate-review/AUTHOR_CONTROLS_REPLAY.py',
    'research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/baseline-skyline-moments-review/source-rerun/controls.py',
    'research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/full-skyline-log-squared-review/author_replay/controls.py',
    'research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/full-skyline-reverse-kl-review/author_replay/controls.py',
    'research/t20-live-20261009/checkpoints/CP11/t20-next-frontier-20261008/skyline-likelihood-score-review/author_replay/controls.py',
    'research/t20-live-20261009/checkpoints/CP12/t20-next-frontier-20261008/sharp-skyline-information-review/author_replay/controls.py',
    'research/t20-live-20261009/checkpoints/CP13/t20-next-frontier-20261008/modal-identity-transport-review/author_controls_snapshot.py',
    'research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/discrimination-replay/verify.py',
)
CHECKPOINT_CODE_PUBLIC_SHA256 = '92f2ff50d1c018312945eeb56a19bc3fe033169f751c35c40c9a662f96931283'
CHECKPOINT_CODE_PUBLIC_PATHS = frozenset(CHECKPOINT_CODE_PUBLIC_MEMBERS)

# Original26 membership stays exact. Every retarget reads and authenticates
# its former coordinate before the original alias, using the same native
# history, current body, mode, index and symlink primitive as the earlier12.
CHECKPOINT_PACKAGE_RETARGETS = (
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction-review/author_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/author_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction/exact_controls.py',
     '4f78222a0ab2d0e4cb4972cb62e110436cc817ed', '92cd73364482270d5acb49190a4f5eb893c4f646aa052281fb2fdbe21c1c2b70', 5030),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/author/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/author/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction/exact_controls.py',
     '4f78222a0ab2d0e4cb4972cb62e110436cc817ed', '92cd73364482270d5acb49190a4f5eb893c4f646aa052281fb2fdbe21c1c2b70', 5030),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/independent/independent_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/independent/independent_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/independent_controls.py',
     'a261bcd23a0263de2df88b14016a58984c234f8a', 'ed2d1faf38772231440c05dc440068abe4849f5a5474a21d890bf6d0502aa1ba', 6836),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/exact_controls.py',
     '4bcf6cd4a98548c23e03a82987bf6ccfad57f1a9', '9ac147575d35266debd88dfd23d91cb2f96cded9823ac85c0e5a109275eea11c', 4780),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/panel_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/panel_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/panel_controls.py',
     'a5b7dfe4518398e7d2cf88ee71b70cc904290365', '0503ae9f04d0b484df886c9123d004ec18953d09c2487b47c91fdf16b2e7435b', 2826),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/exact_controls.py',
     '4bcf6cd4a98548c23e03a82987bf6ccfad57f1a9', '9ac147575d35266debd88dfd23d91cb2f96cded9823ac85c0e5a109275eea11c', 4780),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/panel_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/panel_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/panel_controls.py',
     'a5b7dfe4518398e7d2cf88ee71b70cc904290365', '0503ae9f04d0b484df886c9123d004ec18953d09c2487b47c91fdf16b2e7435b', 2826),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/verify_evidence.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/verify_evidence.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/verify_evidence.py',
     '9c92a346d92a803c528220689b02bdbdd212bd10', '8f41b467eb27f7dea863074e5886f477d0cc02f613a82dbea6e45a4a3d007093', 2252),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/exact_controls.py',
     '4bcf6cd4a98548c23e03a82987bf6ccfad57f1a9', '9ac147575d35266debd88dfd23d91cb2f96cded9823ac85c0e5a109275eea11c', 4780),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/panel_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/panel_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/panel_controls.py',
     'a5b7dfe4518398e7d2cf88ee71b70cc904290365', '0503ae9f04d0b484df886c9123d004ec18953d09c2487b47c91fdf16b2e7435b', 2826),
)
CHECKPOINT_PACKAGE_RETARGETS_SHA256 = 'f1bf97a6313f522d6564f5aea0cc8b9d853556a0b47fef8998481c04dd536534'


# Exactly26 redundant historical package locations, including inert Python
# source. Earlier public bodies preserve their original logical coordinates.
# These paths receive no new public projection or historical execution route.
CHECKPOINT_PACKAGE_COPY_MEMBERS = (
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction-review/REVIEW_RECEIPT.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/REVIEW_RECEIPT.json',
     'c1c324d726adbf696717420bbbd89052b518ebd6', '7731d7ada9d6a4d1ceb456a6af3b90e934f47941ccfd532a73b879af9356a945', 27623),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction-review/SOURCE_AUDIT.md',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/SOURCE_AUDIT.md',
     'e50227b67176b6e5d9033aa9136839e741835e75', '53ecce4670674ef4a8368dc6fb444f737b3d874fb90d81f0fac1c71206cf80d0', 5588),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction-review/SOURCE_BINDINGS.json',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/SOURCE_BINDINGS.json',
     'f05ded2b1580127f42508393f81333d4b2027045', '50b9873dbcc23cb9c9049b69bae22d107bed6873a1a6af8fa33639fa00ad3661', 1126),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction-review/author_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/author_replay/exact_controls.py',
     '4f78222a0ab2d0e4cb4972cb62e110436cc817ed', '92cd73364482270d5acb49190a4f5eb893c4f646aa052281fb2fdbe21c1c2b70', 5030),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction-review/independent_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/independent_controls.py',
     'a261bcd23a0263de2df88b14016a58984c234f8a', 'ed2d1faf38772231440c05dc440068abe4849f5a5474a21d890bf6d0502aa1ba', 6836),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/author/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/author/exact_controls.py',
     '4f78222a0ab2d0e4cb4972cb62e110436cc817ed', '92cd73364482270d5acb49190a4f5eb893c4f646aa052281fb2fdbe21c1c2b70', 5030),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/independent/independent_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/verification_replay/independent/independent_controls.py',
     'a261bcd23a0263de2df88b14016a58984c234f8a', 'ed2d1faf38772231440c05dc440068abe4849f5a5474a21d890bf6d0502aa1ba', 6836),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction-review/verify_review.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction-review/verify_review.py',
     '445665c976901908dbe8d46738819eb947112d53', '3f60c392d2e416c7549e4c76befdc8f48fd137a74509857dcc6495c8c8396e1c', 2224),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction/SOURCE_AUDIT.md',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction/SOURCE_AUDIT.md',
     '4f3879a877879ded9f98efd1e6d5fdbb2ab35c19', '7bf7d837c61ed3c6ef6ecb08270b3b0d345754fb54afcda091aefb96e0d7648a', 6410),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction/exact_controls.py',
     '4f78222a0ab2d0e4cb4972cb62e110436cc817ed', '92cd73364482270d5acb49190a4f5eb893c4f646aa052281fb2fdbe21c1c2b70', 5030),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-absence-obstruction/verify_evidence.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-absence-obstruction/verify_evidence.py',
     '269db84bfcc44d45f7e3c5316d938bff1113a001', '2f1771287858cca17a987faeacb917bc42eed68f98eb62147520b2aa46746d56', 1959),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/exact_controls.py',
     '4bcf6cd4a98548c23e03a82987bf6ccfad57f1a9', '9ac147575d35266debd88dfd23d91cb2f96cded9823ac85c0e5a109275eea11c', 4780),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/panel_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_replay/panel_controls.py',
     'a5b7dfe4518398e7d2cf88ee71b70cc904290365', '0503ae9f04d0b484df886c9123d004ec18953d09c2487b47c91fdf16b2e7435b', 2826),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/exact_controls.py',
     '4bcf6cd4a98548c23e03a82987bf6ccfad57f1a9', '9ac147575d35266debd88dfd23d91cb2f96cded9823ac85c0e5a109275eea11c', 4780),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/panel_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/panel_controls.py',
     'a5b7dfe4518398e7d2cf88ee71b70cc904290365', '0503ae9f04d0b484df886c9123d004ec18953d09c2487b47c91fdf16b2e7435b', 2826),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/verify_evidence.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/author_snapshot/verify_evidence.py',
     '9c92a346d92a803c528220689b02bdbdd212bd10', '8f41b467eb27f7dea863074e5886f477d0cc02f613a82dbea6e45a4a3d007093', 2252),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/independent_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/independent_controls.py',
     '3bd644ae543ef3386cd0331ae9cf3f7b32f7578c', 'cb032a4ca085796e45fc7517d08a02da476a3c78ff46fead87700f9b1c35ea8e', 8975),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/independent_panel_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/independent_panel_controls.py',
     'eb2ac2d153a63b4bddbbec2be44ed31c75b9a070', '748bab6b1445f3740d80e630516a78caf9c4924424bd646a793e0918d31b6c5f', 5498),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/exact_controls.py',
     '4bcf6cd4a98548c23e03a82987bf6ccfad57f1a9', '9ac147575d35266debd88dfd23d91cb2f96cded9823ac85c0e5a109275eea11c', 4780),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/panel_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/verification_replay/panel_controls.py',
     'a5b7dfe4518398e7d2cf88ee71b70cc904290365', '0503ae9f04d0b484df886c9123d004ec18953d09c2487b47c91fdf16b2e7435b', 2826),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor-review/verify_review.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor-review/verify_review.py',
     'b0f1bb39f6ac54624f66b07031c73b692c261b42', '2de38a98bb5ddd27073affa3e2341b9ab3cbb81634efb21f964a93619d454900', 3634),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor/SOURCE_AUDIT.md',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/SOURCE_AUDIT.md',
     '659eebbe5efe9d41589672e9f1cb028522d4db8c', '439a9c0e893dbee30a2e24ea555788251e76fee7e5dd060cfa88049156edf8b6', 6901),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/exact_controls.py',
     '4bcf6cd4a98548c23e03a82987bf6ccfad57f1a9', '9ac147575d35266debd88dfd23d91cb2f96cded9823ac85c0e5a109275eea11c', 4780),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor/panel_controls.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/panel_controls.py',
     'a5b7dfe4518398e7d2cf88ee71b70cc904290365', '0503ae9f04d0b484df886c9123d004ec18953d09c2487b47c91fdf16b2e7435b', 2826),
    ('research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/interaction-calibration-anchor/verify_evidence.py',
     'research/t20-live-20261009/checkpoints/CP05/t20-next-frontier-20261008/interaction-calibration-anchor/verify_evidence.py',
     '9c92a346d92a803c528220689b02bdbdd212bd10', '8f41b467eb27f7dea863074e5886f477d0cc02f613a82dbea6e45a4a3d007093', 2252),
    ('research/t20-live-20261009/checkpoints/CP07/t20-next-frontier-20261008/finite-panel-replay/exact_controls.py',
     'research/t20-live-20261009/checkpoints/CP06/t20-next-frontier-20261008/finite-panel-replay/exact_controls.py',
     '113536080a802c627b68618c3820132e057c30a8', '04cffc5e5d694deb58f64e69f60479afd4a847234b75616c9f5c702d18e72a8b', 4176),
)
CHECKPOINT_PACKAGE_COPY_CATALOG_SHA256 = '344218868b9d7a6cfe55e1468bc37649a0ba9f5bcce78bb40ecbbed4bd5df392'
CHECKPOINT_PACKAGE_COPY_PATHS = frozenset(row[0] for row in CHECKPOINT_PACKAGE_COPY_MEMBERS)


HISTORICAL_PROSE_REVISION = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
HISTORICAL_PROSE = {
    'research/t20-live-20261009/checkpoints/CP19/necessary-truth-operative-basing-20261009/REPORT.md':
        ('15e864dd9b9a31a5203f31fe9b080261afc7de4e',
         '4bd8f0e5bcac178bf9eb890544fcba9fd60f6a1d08cdf2e0cc12bb6d2c4b4c1c', 15381),
    'research/t20-live-20261009/checkpoints/CP19/necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md':
        ('18b3ceb2bcca924387899a9d51f3fd035967eac7',
         '3ccb73001c99c976e728817ca9fca75ab128e6538578068f51333e5321f41b5b', 1939),
    'research/t20-live-20261009/checkpoints/CP20/necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md':
        ('18b3ceb2bcca924387899a9d51f3fd035967eac7',
         '3ccb73001c99c976e728817ca9fca75ab128e6538578068f51333e5321f41b5b', 1939),
    'research/t20-live-20261009/checkpoints/CP20/compound-ground-necessity-20261009/VARIABLE_SHARING_REDUCTION.md':
        ('512266ec363346b6302292f69dafad32f1e067a9',
         '9420d38627e0dea98af9e8838485fb68ab08feb184ae254953f08585cfe2e71d', 1587),
    'research/t20-live-20261009/checkpoints/CP20/compound-ground-necessity-20261009/REPORT.md':
        ('cf657a78f972b7f98190139b2275a3381d288b66',
         '52631c602c1c8fede28dbe6da34480094caf6f441c1aec0293229cdfdf28a0be', 15839),
}
# Capture the original five-path contract before any later finite admissions.
ORIGINAL_HISTORICAL_PROSE_PATHS = tuple(HISTORICAL_PROSE)

# Two independently incorporated mediator bodies have a later exact audit anchor.
# The original five source revisions and their identities remain unchanged.
MEDIATOR_PROSE_REVISION = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
MEDIATOR_COORDINATION = 'experiments/orthemology-v5-successors/source-store/c77bb25b5b3072294a16fb8678441c30a62ec917cad59957193350af80973ff7/BOUNDED_COORDINATION_INFORMATION_v1.md'
MEDIATOR_APPROXIMATION = 'research/t20-v6-20261012/research-v6/type_collective/ROBUST_FINITE_MEDIATOR_BOUND.md'
MEDIATOR_PROSE = {
    MEDIATOR_COORDINATION: ('a949e7e8fdb1fcf386d3580a034d9cb14f34e7d5',
        'c77bb25b5b3072294a16fb8678441c30a62ec917cad59957193350af80973ff7', 13985),
    MEDIATOR_APPROXIMATION: ('8c8b327bb642570307e50ddaef35850b508a80e6',
        '6d8c1b108c74df4638da79a147e6480b6edb9c2b562028c0d17758ab08d45406', 4388),
}
HISTORICAL_PROSE.update(MEDIATOR_PROSE)
HISTORICAL_PROSE_REVISIONS = {
    path: MEDIATOR_PROSE_REVISION if path in MEDIATOR_PROSE else HISTORICAL_PROSE_REVISION
    for path in HISTORICAL_PROSE}
HISTORICAL_PROSE_DISPOSITIONS = {
    path: 'ADD_EXACT' if path == MEDIATOR_APPROXIMATION else 'REUSE'
    for path in HISTORICAL_PROSE}
# This ADD_EXACT source is anchored at its actual original publication,
# independently of the five REUSE sources and two mediator dispositions.
FISHER_PROSE_REVISION = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
FISHER_AUDIT = 'research/t20-v6-20261012/sources/178adaf0d9c8f19f2d0eaf5b8118b157e582b356fa9dddfee6ba8ebe6e5da71b/finite-audit-gradient-classification.md'
HISTORICAL_PROSE[FISHER_AUDIT] = (
    '4dd0bce99ab60c34752bda1e4102341b67350c79',
    '178adaf0d9c8f19f2d0eaf5b8118b157e582b356fa9dddfee6ba8ebe6e5da71b', 29666)
HISTORICAL_PROSE_REVISIONS[FISHER_AUDIT] = FISHER_PROSE_REVISION
HISTORICAL_PROSE_DISPOSITIONS[FISHER_AUDIT] = 'ADD_EXACT'

# Four fully incorporated prose bodies; their formal/review components remain
# current, separate obligations. These literals extend only the finite route.
TYPED_PROSE_REVISION = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
TYPED_PROSE_IDENTITIES = {
    't13-opaque': ('b99fb16058f99ce5db66dd7a02e7515ede5157a002a6e76fc29d0f1bd8d65236',
        'OPAQUE_ATOM_COMPLETENESS_PROOF_v3.md', 'ab7ccee9a98d5a88b8b79a6f0d6a010298bf3204',
        26969, 'identity-src-18324561d5a479234e08'),
    't13-residual': ('7ff286710275b8873e2847ef21b9a30e70c20f465b6bb680569b8f107b484f3e',
        'RESIDUAL_IDENTITY_COMPLETENESS_FEASIBILITY_v1.md', '0692dd6d775e0391498c97c5b77e8c83cf32eb41',
        11482, 'identity-src-36405a21fb515a544d13'),
    't13-bridge': ('02f2ba85547a0798288ec5d307f06fa5b239b8cb9e0faa4b7c7a6ba303097bbe',
        'HYPOTHETICAL_ATOM_APPLICATION_BRIDGE_v2.md', 'a4d90c7d566d79394ca4755bf1d792e810d66880',
        19906, 'identity-src-210a260c6b65330bbabb'),
    't14-separation': ('5d58087eab7e247235ec159abc17f6dc6d5779dc7722518f06d5040b25414e3a',
        'Intensional_Identity_Separation_and_Closed_Identity_Conversion.md', '4920e71de4ac0c17fa8a93f02cd891d65ea8ad74',
        48239, 'identity-src-ae495071a75fcc65a509'),
}
TYPED_SOURCE_KEYS = {key: 'experiments/orthemology-v5-successors/source-store/' + row[0] + '/' + row[1]
                     for key, row in TYPED_PROSE_IDENTITIES.items()}
TYPED_PROSE = {TYPED_SOURCE_KEYS[key]: (row[2], row[0], row[3])
               for key, row in TYPED_PROSE_IDENTITIES.items()}
TYPED_V5_SOURCE_IDS = {TYPED_SOURCE_KEYS[key]: row[4] for key, row in TYPED_PROSE_IDENTITIES.items()}
HISTORICAL_PROSE.update(TYPED_PROSE)
HISTORICAL_PROSE_REVISIONS.update({path: TYPED_PROSE_REVISION for path in TYPED_PROSE})
HISTORICAL_PROSE_DISPOSITIONS.update({path: 'REUSE' for path in TYPED_PROSE})

# Four already incorporated continuation notes migrate only their reader route.
# Their original source/work identities and distinct formal support stay owned
# by the existing crosswalk; the existing public subset is enumerated below.
CONTINUATION_READER_REVISION = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
CONTINUATION_READER_NOTES = {
    'continuation-note-41': (
        'a9eb8521054eb3769ff424037f438ae38f0f0c113d73624efc9d05dea3b35483',
        'ae198b6530ccb5cdce3e15616d939575f7878d28', 13358,
        'continuation-local-rigidity', 'consolidated-common-repair',
        ('continuation-note-40',)),
    'continuation-note-37': (
        '002eab67237670bc990e3762cb0cce1f0de465987ba5aa48a5ccbd27d4ac302e',
        '2804e7b196437dd437f0099b15aa45a76249e63b', 6680,
        'continuation-statistical-repair', 'consolidated-information-and-inquiry',
        ('continuation-note-34',)),
    'continuation-note-28': (
        '4878fd0a4cf6c952af7cdbcb7e8a386c2730ff9986b74b8e39bf9b5077815b0f',
        'f419024deb2a40bf50f7315cdf2dfdde9ede77f6', 15286,
        'continuation-finite-query', 'consolidated-information-and-inquiry',
        ('continuation-note-34',)),
    'continuation-note-31': (
        'b0672a56d007c718a42a7ee6fdc875c915630ad95dff5cfbae7f7e9a419d5349',
        '937f0464dcaa515f1c002a8b36add0c4cb511b42', 5601,
        'continuation-binary-experiment', 'consolidated-information-and-inquiry',
        ('continuation-note-34', 'continuation-note-1')),
}
CONTINUATION_READER_PATHS = {
    key: 'docs/provenance/v5-research-continuations/notes/' + row[0] + '.md'
    for key, row in CONTINUATION_READER_NOTES.items()}
CONTINUATION_READER_PROSE = {
    CONTINUATION_READER_PATHS[key]: (row[1], row[0], row[2])
    for key, row in CONTINUATION_READER_NOTES.items()}
HISTORICAL_PROSE.update(CONTINUATION_READER_PROSE)
HISTORICAL_PROSE_REVISIONS.update({path: CONTINUATION_READER_REVISION
                                  for path in CONTINUATION_READER_PROSE})

# Preserve the accepted sixteen-path contract before the T4 extension.
CONTINUATION_READER_HISTORICAL_PATHS = tuple(HISTORICAL_PROSE)

# Ten incorporated T4 reader aliases, including four support-only sources.
# The other four integrated reviews have no CROSSWALK aliases. The three broad
# accounts remain live; this finite admission neither absorbs nor retires them.
T4_READER_REVISION = 'b4d58482ae00f138782276ee5c4034c48bb2df19'
T4_READER_NOTES = {'continuation-note-83': ('285a7061f8f090946e27e5ff6bd7597b7a0f0472100c7e4b3cb57ea5ac12f6a7',
                          '40d509699e094815d445af4b3fb63cbb1079c4b0',
                          6182,
                          'continuation-beta-budget',
                          'consolidated-information-and-inquiry',
                          ('continuation-note-88', 'continuation-note-86'),
                          ('continuation-beta-rates',)),
 'continuation-note-84': ('3b7cdb283b858339136beb1e0d62cbd32adce0ee9f0562db8961a9f819f52000',
                          'a12e7f7c10894591e1b1e13c26ba99377492563d',
                          2966,
                          'continuation-reporting-clock',
                          'consolidated-information-and-inquiry',
                          ('continuation-note-85', 'continuation-note-90'),
                          ()),
 'continuation-note-85': ('3b8f7d96fa99674b73cb8f822cc3291d455c52879b2f1110630be67660883317',
                          '9715b8685253581e9187c44b2b4a4d81ad74ae73',
                          8219,
                          'continuation-beta-rates',
                          'consolidated-information-and-inquiry',
                          ('continuation-note-83', 'continuation-note-90'),
                          ('continuation-endpoint-density', 'continuation-reporting-clock')),
 'continuation-note-86': ('196728a62cb7bdb24160b33c0ae3627a822f8b2b031fe033e275d6d284efa7df',
                          'af853c549ee6b1b320cf38e14358ded327f9dced',
                          10906,
                          'continuation-all-policy-cost',
                          'consolidated-information-and-inquiry',
                          ('continuation-note-89',),
                          ('continuation-beta-budget',)),
 'continuation-note-87': ('7d3cbeb8bcacdb5d28cb457801ba41de9b21f91542866fe5c5f13a4a632dadd9',
                          '07a1df58ff170334e07261c93af8345093b0f160',
                          14328,
                          'continuation-endpoint-density',
                          'consolidated-information-and-inquiry',
                          ('continuation-note-85', 'continuation-note-90'),
                          ()),
 'continuation-note-88': ('826c824188b79a5e734c77f4aaa24f5ecf15d1a73e7af0d68ad8b8955bb674ab',
                          'fbd42a9270e356e4c361695ea28df58aaba773c9',
                          6121,
                          None,
                          'consolidated-information-and-inquiry',
                          None,
                          ('continuation-beta-budget',)),
 'continuation-note-89': ('575700cb383a6f0849e2a952ba6652e6de75920eb74ebcb9a7eb0ed21517a696',
                          '9be9a40bb2d6b3a4e94d6e06ae8e68b8b3198bda',
                          5443,
                          None,
                          'consolidated-information-and-inquiry',
                          None,
                          ('continuation-all-policy-cost',)),
 'continuation-note-92': ('b092780b29dd9fa00ac276142b090a5b8b88da79da9c278268264669e08f3d8c',
                          '4e69862256f3014f8e94d528b13ff0f63dd7f3eb',
                          29013,
                          'continuation-markov',
                          'consolidated-collective-inquiry',
                          ('continuation-note-96', 'continuation-note-97'),
                          ()),
 'continuation-note-96': ('34c1f25cd1144b386ff4c70a2fbfacc7da2a0fc87f5cd78b430badf260ab49f6',
                          '6bcd9f7c0faea3fe3037c1f188288555312517b1',
                          1017,
                          None,
                          'consolidated-collective-inquiry',
                          None,
                          ('continuation-markov',)),
 'continuation-note-97': ('9438fdcbea8747c7e5599483096eca9541cfdf673d6a96866c019c5ced06519a',
                          '80e45c60c8f4e71a8191f906d04afd4ab0384b06',
                          11145,
                          None,
                          'consolidated-collective-inquiry',
                          None,
                          ('continuation-markov',))}
T4_READER_PATHS = {
    key: 'docs/provenance/v5-research-continuations/notes/' + row[0] + '.md'
    for key, row in T4_READER_NOTES.items()}
T4_READER_PROSE = {T4_READER_PATHS[key]: (row[1], row[0], row[2])
                   for key, row in T4_READER_NOTES.items()}
T4_READER_SUPPORT_PROSE = {T4_READER_PATHS[key] for key, row in T4_READER_NOTES.items()
                          if row[3] is None}
HISTORICAL_PROSE.update(T4_READER_PROSE)
HISTORICAL_PROSE_REVISIONS.update({path: T4_READER_REVISION for path in T4_READER_PROSE})

# Preserve the accepted twenty-six-path contract before the next24 extension.
T4_READER_HISTORICAL_PATHS = tuple(HISTORICAL_PROSE)

# Twenty-four incorporated public originals. Three retain CROSSWALK aliases;
# only the nudge audit and formal-scope register are T20 public-manifest forms.
# Archive originals, execution receipts and removal authority are separate.
NEXT24_REVISION = 'd0abc116b51f04c064fc60ebbdd511b63a795f45'
NEXT24_NOTES = {1: ('e46c8d347ed1864c6c65270b0b7e90eef0146815804bb9f783fa465cd3fbc8bc',
     'a95a68888f591e035b04baa14075445fd25325b7',
     4411,
     'consolidated-common-repair'),
 2: ('b0ec9163de7f6deb49f44bb10ef1f279151ee78a30b9d2dd7ca9736d8bb62750',
     '7d1536017f2dd2a22a2137f05c9cde0820908787',
     12456,
     'consolidated-common-repair'),
 3: ('ad15c28206a020cc7c063c17309d6bd3c05e182377a398c7507875523df7feb4',
     '848f8f45967ddc66c76550ec2b44d233ba7966e9',
     5091,
     'consolidated-information-and-inquiry'),
 4: ('1b7488aeafc74b7115479a8cf73c0abf04d89c3924109aa922ee6099e32be2d8',
     '2c9205fdd87f3702af3e238f5cfd1b6240013ee4',
     11570,
     'consolidated-information-and-inquiry'),
 5: ('9e00aaaaa63828e05d252e134dc225e2718461540301138a30567fbb63a24eb9',
     'bcf29dd85a92b76483cbeacd9a6fd63343687dc1',
     6770,
     'consolidated-information-and-inquiry'),
 6: ('4f3d54cd93718e479f1485c182058bcd5ee40c13e4b9f598e4a011e6a92adaa0',
     'd981100cdefce3b7534ce08c599b0706e5b2a231',
     9552,
     'consolidated-common-repair'),
 7: ('3efb043df2749e965a70ae815003952d0f7e3c1d203d4e04e04e24fd0892a20c',
     '4d2aafcd49f2b088cb4afebdb67846cece5f922b',
     6124,
     'consolidated-common-repair'),
 8: ('5c9fcd3012d9c41bc951cf78e2ccc29591ab8151a0037e6cd0ff07cabb0e54f4',
     'bd414fc2b16dcd53116d3ed772e27b3c792237c2',
     6384,
     'consolidated-common-repair'),
 9: ('36bf84b786280660b3ec4a5e3a110f04d98598cdbe49e7680a438de344a0dd06',
     'f43d9ffc34ad19eb1e4d14cb1a176a916d408a36',
     7718,
     'consolidated-common-repair'),
 10: ('1fa9f620cbab16c728d931520d777e8ef25090c52520dca39144ed43e2790459',
      'cbf93e2e9912045c58946dc8a936e54c2dff5b95',
      5847,
      'consolidated-common-repair'),
 11: ('673111801ec83a2118743de3cd851f7a3db8e6c9580750f3fe766a9626b0f498',
      '8cfcd82cce15b5df64f964f81b2424c97fc1bb7c',
      9541,
      'consolidated-information-and-inquiry'),
 12: ('bd5e18cb3616a7ead45cc407da8ebe72274358edcd12459f4109ad155e2f53b2',
      'dd8f4908d7a733aa8f08481da568318d458fc584',
      4770,
      'consolidated-information-and-inquiry'),
 13: ('50cf2306b486db59fd7a2ecf77d07b3b54c3e486745f0b7308cb091de1c3ec61',
      '1f0bf3a48055fed1aa24dcfbba617d855d9c3c2e',
      15300,
      'consolidated-information-and-inquiry'),
 14: ('1f97b7f6e879f4ebe42b26620aac0c75095345f4ec65bfe2979ecd32aa538dbf',
      '952acfcb7a6f7e52731ff3b26c85dd5362a0e4f1',
      4995,
      'consolidated-information-and-inquiry'),
 15: ('e6be2257c2dabfd15057f1c59603518d1ba20976068579bd31512ec1f5bfafce',
      '00dcece21824577e981a8dd1c103056fea60e0a0',
      5605,
      'consolidated-information-and-inquiry'),
 16: ('ad4909aa4015f759a7494c5a0b5ddfa0c4ccaaf6d14ad7c89386db53e01385d6',
      '4a91c34083b0df5658a437fdf86a471471524b30',
      5551,
      'consolidated-information-and-inquiry'),
 17: ('63494364aeb423cecee01e1b347a4dfed7e2c4b544c90d456465520378810d40',
      '1cc325aad1ee71001f5f4c7eb2881211d78a56df',
      7100,
      'consolidated-information-and-inquiry'),
 18: ('18c1e07537712caaadf60d6bf8f25272aaf8c1767722bd56b3b5f1ed7258ee73',
      '38e462ee8c12a50cce8fd6bccf5ca3dde2597458',
      10150,
      'consolidated-information-and-inquiry'),
 19: ('71899f46c0346c901fd19697436beaa511b9814f879835604bbe23264d062aeb',
      '75476c99f17cf81258a6066bd12e2802c9f32f99',
      5518,
      'consolidated-information-and-inquiry'),
 20: ('51c98ce4cbc011f1e4d4d2af7fa9a34319f53713b876977bc9b16c74f0e258dc',
      '772e3d5300525c24c56da93fd2574ce4d4a1e1a0',
      3154,
      'consolidated-information-and-inquiry'),
 21: ('890c6bc8949f630878e9d3de6bed22c7070d0b4f0d7c43d7fa96f4c7a6d91607',
      'd2f19e3562852bbb3fc0d849e421921949fddacb',
      10678,
      'consolidated-information-and-inquiry'),
 22: ('71156aa5eb3f520e004fd15b3c8eb5a994bbf87c9735c00e0ea9c921f409e10e',
      '75bb17ddd69e37db6530357307078d056b97ec16',
      16844,
      'consolidated-common-repair'),
 23: ('45ffbb9679d23bd16a43b4930ec615bb55f4c0c56705e5a0c90f0fec425a2a3e',
      '02390e5f62fc4f5ab97263fa548b56f412c17ce3',
      9045,
      'consolidated-common-repair'),
 24: ('21f9e48328bfbf843b5f0371168f84c51768dec6260b3798fca4a461900aa006',
      'b5f6e9140796030880f6dbc723514bfb393d23c2',
      18202,
      'consolidated-objective-normativity')}
NEXT24_PATHS = {
    n: 'docs/provenance/v5-research-continuations/notes/' + row[0] + '.md'
    for n, row in NEXT24_NOTES.items()}
NEXT24_PROSE = {NEXT24_PATHS[n]: (row[1], row[0], row[2])
                for n, row in NEXT24_NOTES.items()}
NEXT24_PUBLIC_PROSE = {NEXT24_PATHS[9], NEXT24_PATHS[22]}
NEXT24_SUPPORT_PROSE = {NEXT24_PATHS[22]}
NEXT24_READER_ALIASES = {
    19: ('continuation-note-27', 'continuation-common-observation', 'research-note',
         ('continuation-note-1',), ()),
    22: ('continuation-note-40', None, None, None,
         ('continuation-anchor-repair', 'continuation-dependency-quadratic',
          'continuation-local-approximate', 'continuation-local-rigidity',
          'continuation-nudge', 'continuation-smooth-blocks',
          'continuation-smooth-rigidity', 'continuation-source-bridge')),
    24: ('continuation-note-48', 'continuation-source-bridge', 'synthesis',
         ('continuation-note-40', 'continuation-note-39', 'continuation-note-35'), ()),
}
HISTORICAL_PROSE.update(NEXT24_PROSE)
HISTORICAL_PROSE_REVISIONS.update({path: NEXT24_REVISION for path in NEXT24_PROSE})
HISTORICAL_PROSE_DISPOSITIONS.update({path: 'REUSE' for path in NEXT24_PUBLIC_PROSE})

# Exact incorporated sparse-prior public originals; no new public manifest forms.
EARLIER_FIFTY_HISTORICAL_PATHS = tuple(HISTORICAL_PROSE)
SPARSE_PRIOR_REVISION = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
SPARSE_PRIOR_PROSE = {'docs/provenance/v5-research-continuations/notes/0ba213e9f1cd5c985925864d7edcc505c3adb16fa30036338b39ad04b77ea54f.md': ('4de8b1921235006c37ae00945fad3e6e328d6336',
                                                                                                                         '0ba213e9f1cd5c985925864d7edcc505c3adb16fa30036338b39ad04b77ea54f',
                                                                                                                         1607),
 'docs/provenance/v5-research-continuations/notes/22c70614cb4a011790e348461f3e2fbea5e13b2eeb788dcd2124560fb0ef0f07.md': ('d82e2625487cf0771f96f3a883170f7edd7bd919',
                                                                                                                         '22c70614cb4a011790e348461f3e2fbea5e13b2eeb788dcd2124560fb0ef0f07',
                                                                                                                         2703),
 'docs/provenance/v5-research-continuations/notes/236f78b5ecc313f47085a765f26ef2f0482fdaff154c2aebb7393a8c01c59236.md': ('3f1ebe731980b67b94945f58689999b5b4edf55d',
                                                                                                                         '236f78b5ecc313f47085a765f26ef2f0482fdaff154c2aebb7393a8c01c59236',
                                                                                                                         4625),
 'docs/provenance/v5-research-continuations/notes/251394f394fe75f9062aaa4dea33da2b3ffa3370572e14ba60e52ceb1c68a30b.md': ('32e1bec0ba44d1f558286b0d5878d2f482b9907e',
                                                                                                                         '251394f394fe75f9062aaa4dea33da2b3ffa3370572e14ba60e52ceb1c68a30b',
                                                                                                                         8764),
 'docs/provenance/v5-research-continuations/notes/3cdf7cb6582b44a2198ce9527847416ee834aa7636999871081e1677600a9f60.md': ('ead60afbdc6f47c99c8aa17403daab4f9f602083',
                                                                                                                         '3cdf7cb6582b44a2198ce9527847416ee834aa7636999871081e1677600a9f60',
                                                                                                                         2311),
 'docs/provenance/v5-research-continuations/notes/6b796642b23d6280cfec717f7a762a55fe76a2fbc67b16f6c6b0fc1008599476.md': ('9bd1c1e0e30b46800c04c6dd189e40066b6ed4a6',
                                                                                                                         '6b796642b23d6280cfec717f7a762a55fe76a2fbc67b16f6c6b0fc1008599476',
                                                                                                                         8765),
 'docs/provenance/v5-research-continuations/notes/767be5173842b1520af940db691120091d868677754e7b452a0c7467ece4665d.md': ('b64eac11f5d5efd6618219731d6fa543d3c73487',
                                                                                                                         '767be5173842b1520af940db691120091d868677754e7b452a0c7467ece4665d',
                                                                                                                         7472),
 'docs/provenance/v5-research-continuations/notes/87cad31677966946661ca6effed55165db3505d1bca45bfa6ba2428946cca88c.md': ('40d69b1e5e377cab279f1d662cffcab0f1481378',
                                                                                                                         '87cad31677966946661ca6effed55165db3505d1bca45bfa6ba2428946cca88c',
                                                                                                                         5124),
 'docs/provenance/v5-research-continuations/notes/893aabc2774f6a31df5777a9dab8cc4de2840a2f01d95691ce913f0406ab489c.md': ('dd884420d315600cc7273536e8b70d48e5d3c3dd',
                                                                                                                         '893aabc2774f6a31df5777a9dab8cc4de2840a2f01d95691ce913f0406ab489c',
                                                                                                                         6175),
 'docs/provenance/v5-research-continuations/notes/99847d69a9a9df978a7e596cc35b75b744e7661b72dd514d29bc3cf4d897cc6c.md': ('e47ed15533018067e34c25ab30a659386a02d043',
                                                                                                                         '99847d69a9a9df978a7e596cc35b75b744e7661b72dd514d29bc3cf4d897cc6c',
                                                                                                                         4740),
 'docs/provenance/v5-research-continuations/notes/9c7508259cb9916b1ba6b0557584cff186487d256dac3918269052b4cd5626b6.md': ('db0f92e4868eb7a8df168ba69f53fce74a54f65e',
                                                                                                                         '9c7508259cb9916b1ba6b0557584cff186487d256dac3918269052b4cd5626b6',
                                                                                                                         1387),
 'docs/provenance/v5-research-continuations/notes/b0edcf2ebfe71957a789033dec063424e658fe8971ef28e1f2fe9a4956e5d18e.md': ('5f7789f7cbd38d8045e95154a00f5e2196b63134',
                                                                                                                         'b0edcf2ebfe71957a789033dec063424e658fe8971ef28e1f2fe9a4956e5d18e',
                                                                                                                         2448),
 'docs/provenance/v5-research-continuations/notes/b1a029f0cd442ff623d9783c15e09260cd6063bf976290010b3fba07ec0548bf.md': ('04a057f0604fcd9de9be11443113df5636510b19',
                                                                                                                         'b1a029f0cd442ff623d9783c15e09260cd6063bf976290010b3fba07ec0548bf',
                                                                                                                         4114),
 'docs/provenance/v5-research-continuations/notes/b3403229c91a718f3e8c61068649590ec090d208206d9922da2270f71e956658.md': ('c45b5a4f02d336ff00230e07d155b043874c4eca',
                                                                                                                         'b3403229c91a718f3e8c61068649590ec090d208206d9922da2270f71e956658',
                                                                                                                         10334),
 'docs/provenance/v5-research-continuations/notes/b545637a8dc1bdfda4a949dfe3a6084b469c5ef8639af8ae97b8e5fef683e0d3.md': ('ab2e9c125c1a65714e3a0670043f65859f299774',
                                                                                                                         'b545637a8dc1bdfda4a949dfe3a6084b469c5ef8639af8ae97b8e5fef683e0d3',
                                                                                                                         9202),
 'docs/provenance/v5-research-continuations/notes/b6a6db5048293e4de7f286689ea635448ea61aec5f9a08acff0968892e10b5bb.md': ('ab8e4a2149efeee43a943db37d0e51eb144200b3',
                                                                                                                         'b6a6db5048293e4de7f286689ea635448ea61aec5f9a08acff0968892e10b5bb',
                                                                                                                         5703),
 'docs/provenance/v5-research-continuations/notes/c079f7733904976a602adae47284062ad23141dd9c79b04652e3561e74692a50.md': ('9701a6c26c8419e2cd01db4a86a2db47af28659d',
                                                                                                                         'c079f7733904976a602adae47284062ad23141dd9c79b04652e3561e74692a50',
                                                                                                                         10353),
 'docs/provenance/v5-research-continuations/notes/cab3e124b6ef2faad2c945c20d22d50e7fc2d1455367bcd4cb6dcf633908b3b9.md': ('885d647840476099ca58a0a9b8f0ca6474033164',
                                                                                                                         'cab3e124b6ef2faad2c945c20d22d50e7fc2d1455367bcd4cb6dcf633908b3b9',
                                                                                                                         2872),
 'docs/provenance/v5-research-continuations/notes/d519d3b51e5f03f7b55db3c22c2a423bdb6cf5a702e726e4a57459e527ab8dbd.md': ('093d47e908d27ac854b722d059d2bf6ee14f2ce7',
                                                                                                                         'd519d3b51e5f03f7b55db3c22c2a423bdb6cf5a702e726e4a57459e527ab8dbd',
                                                                                                                         11197),
 'docs/provenance/v5-research-continuations/notes/daa7e92aaeee1cc9ae5601877a01ddfbb8ce2cf9cabf3f4f693ec8a7c8a0893b.md': ('05d1ee82e1cea6db4639dc96147571642a9b6f19',
                                                                                                                         'daa7e92aaeee1cc9ae5601877a01ddfbb8ce2cf9cabf3f4f693ec8a7c8a0893b',
                                                                                                                         7244),
 'docs/provenance/v5-research-continuations/notes/e2afa027d652771010f909eb34642d5512c102a34c85a0ef90ff466b9fd7e0ae.md': ('1442f0674ffe32f5a50d146993d4b3ac585e07c4',
                                                                                                                         'e2afa027d652771010f909eb34642d5512c102a34c85a0ef90ff466b9fd7e0ae',
                                                                                                                         5928),
 'docs/provenance/v5-research-continuations/notes/e2cf470975d1d6f344d3dd788410c911b5d6f9d93fa528709339322bcb4d8f6b.md': ('0639e32fb2b0d4128e64738030a546bdb1589374',
                                                                                                                         'e2cf470975d1d6f344d3dd788410c911b5d6f9d93fa528709339322bcb4d8f6b',
                                                                                                                         5715),
 'docs/provenance/v5-research-continuations/notes/e40d89c1d65f9053bafc6aea41ba93af0b510586ba188e14ba5a8f6d9a50c71f.md': ('7e33cd9283868e0bce24c38758c0d77c2a190666',
                                                                                                                         'e40d89c1d65f9053bafc6aea41ba93af0b510586ba188e14ba5a8f6d9a50c71f',
                                                                                                                         6541),
 'docs/provenance/v5-research-continuations/notes/f0fe93679a7c062a452bd3b3b2615c886dcdf8b96579af2d1ddd2c17c6df6459.md': ('a9f27e973a15d6cddc4d5ccbc20457a811e21ac9',
                                                                                                                         'f0fe93679a7c062a452bd3b3b2615c886dcdf8b96579af2d1ddd2c17c6df6459',
                                                                                                                         1437),
 'docs/provenance/v5-research-continuations/notes/f7f610f5225df88d97fb6a60f984a7ec976632697e2e3f7854f4777994601d4a.md': ('8ba4cb61febc35bffee4862c0cfa0b0ac67f3bd1',
                                                                                                                         'f7f610f5225df88d97fb6a60f984a7ec976632697e2e3f7854f4777994601d4a',
                                                                                                                         9310)}
SPARSE_PRIOR_READER_ALIASES = {'continuation-note-118': ('docs/provenance/v5-research-continuations/notes/22c70614cb4a011790e348461f3e2fbea5e13b2eeb788dcd2124560fb0ef0f07.md',
                           None,
                           None,
                           None,
                           ('continuation-prior-transport',)),
 'continuation-note-120': ('docs/provenance/v5-research-continuations/notes/e40d89c1d65f9053bafc6aea41ba93af0b510586ba188e14ba5a8f6d9a50c71f.md',
                           None,
                           None,
                           None,
                           ('continuation-prior-transport',)),
 'continuation-note-138': ('docs/provenance/v5-research-continuations/notes/b3403229c91a718f3e8c61068649590ec090d208206d9922da2270f71e956658.md',
                           'continuation-cluster-smoothing',
                           'research-note',
                           (),
                           ()),
 'continuation-note-133': ('docs/provenance/v5-research-continuations/notes/99847d69a9a9df978a7e596cc35b75b744e7661b72dd514d29bc3cf4d897cc6c.md',
                           None,
                           None,
                           None,
                           ('continuation-critical-uniform',
                            'continuation-interior-contamination',
                            'continuation-strict-width')),
 'continuation-note-134': ('docs/provenance/v5-research-continuations/notes/3cdf7cb6582b44a2198ce9527847416ee834aa7636999871081e1677600a9f60.md',
                           None,
                           None,
                           None,
                           ('continuation-critical-uniform',
                            'continuation-interior-contamination',
                            'continuation-strict-width')),
 'continuation-note-145': ('docs/provenance/v5-research-continuations/notes/767be5173842b1520af940db691120091d868677754e7b452a0c7467ece4665d.md',
                           'continuation-strict-width',
                           'research-note',
                           ('continuation-note-133', 'continuation-note-134', 'continuation-note-136'),
                           ()),
 'continuation-note-136': ('docs/provenance/v5-research-continuations/notes/d519d3b51e5f03f7b55db3c22c2a423bdb6cf5a702e726e4a57459e527ab8dbd.md',
                           None,
                           None,
                           None,
                           ('continuation-strict-width',)),
 'continuation-note-141': ('docs/provenance/v5-research-continuations/notes/e2afa027d652771010f909eb34642d5512c102a34c85a0ef90ff466b9fd7e0ae.md',
                           'continuation-critical-uniform',
                           'research-note',
                           ('continuation-note-133', 'continuation-note-134'),
                           ()),
 'continuation-note-139': ('docs/provenance/v5-research-continuations/notes/c079f7733904976a602adae47284062ad23141dd9c79b04652e3561e74692a50.md',
                           'continuation-contamination-crossover',
                           'research-note',
                           (),
                           ()),
 'continuation-note-143': ('docs/provenance/v5-research-continuations/notes/b1a029f0cd442ff623d9783c15e09260cd6063bf976290010b3fba07ec0548bf.md',
                           'continuation-interior-contamination',
                           'research-note',
                           ('continuation-note-133', 'continuation-note-134'),
                           ()),
 'continuation-note-148': ('docs/provenance/v5-research-continuations/notes/236f78b5ecc313f47085a765f26ef2f0482fdaff154c2aebb7393a8c01c59236.md',
                           None,
                           None,
                           None,
                           ('continuation-rational-prior',)),
 'continuation-note-150': ('docs/provenance/v5-research-continuations/notes/cab3e124b6ef2faad2c945c20d22d50e7fc2d1455367bcd4cb6dcf633908b3b9.md',
                           None,
                           None,
                           None,
                           ('continuation-rational-prior',)),
 'continuation-note-146': ('docs/provenance/v5-research-continuations/notes/251394f394fe75f9062aaa4dea33da2b3ffa3370572e14ba60e52ceb1c68a30b.md',
                           None,
                           None,
                           None,
                           ('continuation-rational-prior',)),
 'continuation-note-149': ('docs/provenance/v5-research-continuations/notes/6b796642b23d6280cfec717f7a762a55fe76a2fbc67b16f6c6b0fc1008599476.md',
                           'continuation-rational-prior',
                           'research-software',
                           ('continuation-note-148',
                            'continuation-note-150',
                            'continuation-note-146',
                            'prior-rational-reference'),
                           ()),
 'continuation-note-160': ('docs/provenance/v5-research-continuations/notes/b6a6db5048293e4de7f286689ea635448ea61aec5f9a08acff0968892e10b5bb.md',
                           None,
                           None,
                           None,
                           ('continuation-observed-loss',))}
SPARSE_PRIOR_SUPPORT_PROSE = {row[0] for row in SPARSE_PRIOR_READER_ALIASES.values() if row[1] is None}
SPARSE_PRIOR_ORIGINAL_SOURCE_MAP = ('0f565ab802d53fae8a3a929e65f291e3dade7242', 'a6c2c87082f27c8560cfb4790059cc242effb5f45e3f7bdf30adf8b722b808c7', 5990901)
HISTORICAL_PROSE.update(SPARSE_PRIOR_PROSE)
HISTORICAL_PROSE_REVISIONS.update({path: SPARSE_PRIOR_REVISION for path in SPARSE_PRIOR_PROSE})

# These six notes already have public REUSE rows. Their original coordinates
# can be pinned without publishing any other reader-only or held source.
PUBLIC_READER_NOTE_PATHS = (
    *(CONTINUATION_READER_PATHS[key] for key in
      ('continuation-note-37', 'continuation-note-28')),
    *(T4_READER_PATHS[key] for key in
      ('continuation-note-87', 'continuation-note-92',
       'continuation-note-96', 'continuation-note-97')),
)
HISTORICAL_PROSE_DISPOSITIONS.update({path: 'REUSE' for path in PUBLIC_READER_NOTE_PATHS})
CONTINUATION_REGISTRY_PATH = 'experiments/orthemology-v5-continuations/registry.json'
CONTINUATION_REGISTRY_REVISION = HISTORICAL_PROSE_REVISION

TYPED_GUIDES = {
    'experiments/orthemology-v5-successors/groups/t13-identity/README.md': (
        '0d228b107878098508dc31368517ac07fe688dff',
        '9492d888f684355f2f72f15e1da7ddca3525b2523e3a670c2da25d811c6eaf96', 7880,
        {'t13-opaque': 1, 't13-residual': 2, 't13-bridge': 1}),
    'experiments/orthemology-v5-successors/groups/t14-identity/README.md': (
        '09ea18f06905c0e5116375b2163737cf380755eb',
        'bd58d620ac8a0dd0bbd8a3eb51e0c254b73cf14ae795a48dc19c347ee69b9961', 16523,
        {'t14-separation': 5}),
}

MEDIATOR_GUIDE = 'experiments/orthemology-v5-successors/groups/t12-written/README.md'
MEDIATOR_GUIDE_BLOB = '7c6a9bfdeaf8372d3ea73ff8a06f4aefb17ef838'
MEDIATOR_GUIDE_SHA256 = 'e86297f6ff2e0b8abce4fd8d1fe66e57c64e43e83ecec664422b4ed7abf3440e'
MEDIATOR_GUIDE_BYTES = 18763

# The inherited duplicate is a path obligation, not an extra manifest object.
HISTORICAL_PROSE_PUBLIC_PATHS = tuple(
    path for path in HISTORICAL_PROSE
    if path not in SPARSE_PRIOR_PROSE
    and path != 'research/t20-live-20261009/checkpoints/CP20/necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md'
    and ((path not in CONTINUATION_READER_PROSE and path not in T4_READER_PROSE)
         or path in PUBLIC_READER_NOTE_PATHS)
    and (path not in NEXT24_PROSE or path in NEXT24_PUBLIC_PROSE))


def historical_source_bytes(root, path, revision, git_blob):
    """Authenticate one finite original and reject any unsafe or wrong copy.

    Missing physical prose may use the pinned original Git object. A present
    copy must still match. No source is written, no fallback follows a failed
    read, and these checks do not qualify custody or historical execution.
    """
    binding = HISTORICAL_PROSE.get(path)
    if not binding or revision != HISTORICAL_PROSE_REVISIONS[path] or git_blob != binding[0]:
        raise ValueError('unqualified historical prose binding')
    root = pathlib.Path(root)
    if path in MEDIATOR_PROSE:
        require_mediator_context(root)
    elif path == FISHER_AUDIT:
        require_fisher_context(root)
    elif path in TYPED_PROSE:
        require_typed_context(root)
    elif path in CONTINUATION_READER_PROSE:
        require_continuation_note_context(root)
    elif path in T4_READER_PROSE:
        require_t4_note_context(root)
    elif path in NEXT24_PROSE:
        require_next24_note_context(root)
    elif path in SPARSE_PRIOR_PROSE:
        require_sparse_prior_context(root)
    blob, identity, size = binding

    def git(*args):
        result = subprocess.run(
            ['git', '--no-replace-objects', '--literal-pathspecs', *args],
            cwd=root, capture_output=True, check=False)
        if result.returncode:
            raise ValueError('required historical Git objects unavailable')
        return result.stdout

    if git('cat-file', '-t', revision) != b'commit\n':
        raise ValueError('historical revision is not the pinned commit')
    expected_entry = ('100644 blob ' + blob + '\t' + path + '\0').encode()
    if git('ls-tree', '-z', revision, '--', path) != expected_entry:
        raise ValueError('historical path, blob or mode differs')
    body = git('cat-file', 'blob', blob)
    raw = b'blob ' + str(len(body)).encode() + b'\0' + body
    if (len(body), digest(body), hashlib.sha1(raw).hexdigest()) != (size, identity, blob):
        raise ValueError('historical source bytes differ')

    # A combined baseline/worktree diff can show D while the index contains a
    # wrong blob, mode or unresolved merge. Bind the actual staged original too.
    indexed = git('ls-files', '--stage', '-z', '--', path)
    expected_index = ('100644 ' + blob + ' 0\t' + path + '\0').encode()
    if indexed not in (b'', expected_index):
        raise ValueError('historical source index is conflicted or differs from its pinned original')

    target, entry = root, None
    parts = path.split('/')
    for index, part in enumerate(parts):
        target = target / part
        try:
            entry = target.lstat()
        except FileNotFoundError:
            entry = None
            continue
        if stat.S_ISLNK(entry.st_mode):
            raise ValueError('historical source path contains a symlink')
        if index < len(parts) - 1 and not stat.S_ISDIR(entry.st_mode):
            raise ValueError('historical source ancestor is not a directory')
    if entry is not None:
        if not stat.S_ISREG(entry.st_mode) or entry.st_mode & 0o111:
            raise ValueError('historical source is not a regular nonexecutable file')
        if target.read_bytes() != body:
            raise ValueError('present historical source differs from its pinned edition')
    return body



def require_sparse_prior_context(root):
    """Bind the incorporated originals to their exact prior roles and current work.

    This is finite source integrity, not scientific adoption, fresh execution,
    independent custody or authority to remove a production original.
    """
    root = pathlib.Path(root)
    try:
        owners = json.loads(_regular_current_bytes(root,
            'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'))
        cross = json.loads(_regular_current_bytes(root,
            'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'))
        bindings = owners['historical_source_bindings']
        fields = {'path', 'repository_revision', 'git_blob', 'role', 'reading_source', 'basis'}
        if (not isinstance(bindings, list)
                or any(not isinstance(row, dict) or set(row) != fields for row in bindings)
                or len(bindings) != len(HISTORICAL_PROSE)
                or {row['path'] for row in bindings} != set(HISTORICAL_PROSE)):
            raise ValueError('the complete earlier fifty and sparse-prior twenty-five bindings are required')
        for path, (blob, identity, size) in SPARSE_PRIOR_PROSE.items():
            expected = dict(path=path, repository_revision=SPARSE_PRIOR_REVISION,
                git_blob=blob, role='historical-source', reading_source='consolidated-information-and-inquiry',
                basis='scientific-consolidation-review')
            if [row for row in bindings if row['path'] == path] != [expected]:
                raise ValueError('the exact sparse-prior original owner binding is required')
            names = [key for key, row in cross['sources'].items() if row['path'] == path]
            declared = [key for key, row in SPARSE_PRIOR_READER_ALIASES.items() if row[0] == path]
            if names != declared:
                raise ValueError('sparse-prior source aliases differ from their original population')
        for key, path, role in (
                ('consolidated-information-and-inquiry', 'mathematics/information-and-inquiry.md', 'work-source'),
                ('scientific-consolidation-review', 'docs/scientific-consolidation-review.md', 'review')):
            selected = [row for row in owners['source_additions'] if row['key'] == key]
            if len(selected) != 1:
                raise ValueError('missing or duplicate current sparse-prior reading owner')
            admission, source = selected[0], cross['sources'][key]
            body = _regular_current_bytes(root, path)
            oid = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
            expected_index = ('100644 ' + oid + ' 0\t' + path + '\0').encode()
            if (admission['path'] != path or source['path'] != path or admission['role'] != role
                    or admission['mode'] != '100644' or admission['git_oid'] != oid
                    or admission['bytes'] != len(body) or admission['sha256'] != digest(body)
                    or source['sha256'] != digest(body)
                    or _continuation_git(root, 'ls-files', '--stage', '-z', '--', path) != expected_index):
                raise ValueError('current sparse-prior scholarship or review edition differs')
            if role == 'work-source' and 'scientific-consolidation-review' not in admission['supporting_source_keys']:
                raise ValueError('current sparse-prior work has lost its review owner')
        for key, (path, work, role, support, users) in SPARSE_PRIOR_READER_ALIASES.items():
            source = cross['sources'][key]
            primary = [row for row in cross['works'] if key in row.get('source_keys', [])]
            forms = [form for row in cross['works'] for form in row.get('reading_forms', [])
                     if form.get('source') == key]
            supported = sorted(row['key'] for row in cross['works']
                               if key in row.get('supporting_source_keys', []))
            expected_form = {'source': key, 'relationship': 'historical-source'}
            if work is None:
                if primary or forms or support is not None or role is not None:
                    raise ValueError('sparse-prior support-only original acquired a work or reading form')
            elif (len(primary) != 1 or primary[0]['key'] != work or primary[0]['role'] != role
                    or primary[0]['source_keys'] != [key] or primary[0]['reading_forms'] != [expected_form]
                    or forms != [expected_form] or primary[0].get('supporting_source_keys', []) != list(support)
                    or any(name not in cross['sources'] for name in support)):
                raise ValueError('sparse-prior original work role or retained support differs')
            relation = {'from': key, 'to': 'consolidated-information-and-inquiry',
                        'kind': 'logical-content-incorporated-historical-source-retained',
                        'basis': 'scientific-consolidation-review'}
            if (source['sha256'] != SPARSE_PRIOR_PROSE[path][1] or supported != list(users)
                    or not isinstance(source.get('read_scope'), str) or not source['read_scope'].strip()
                    or [row for row in cross['relations'] if row.get('from') == key] != [relation]
                    or any(key in row.get('source_keys', []) for row in cross['reader_journeys'])):
                raise ValueError('sparse-prior source identity, support incidence or incorporation differs')
    except (KeyError, TypeError, UnicodeError) as exc:
        raise ValueError('invalid current sparse-prior source context') from exc


def sparse_prior_source_bytes(root, row):
    """Read one original public occurrence without changing its historical role.

    The original map supplies archive/member/derivation identity; the finite
    prose route supplies native original bytes and current reading ownership.
    Existing result, review, failure and status associations remain intact.
    """
    if not isinstance(row, dict) or row.get('path') not in SPARSE_PRIOR_PROSE:
        raise ValueError('unqualified sparse-prior source occurrence')
    path = 'docs/provenance/v5-research-continuations/SOURCE_MAP.json'
    blob, identity, size = SPARSE_PRIOR_ORIGINAL_SOURCE_MAP
    expected = ('100644 blob ' + blob + '\t' + path + '\0').encode()
    if _continuation_git(root, 'ls-tree', '-z', SPARSE_PRIOR_REVISION, '--', path) != expected:
        raise ValueError('sparse-prior original source map coordinate differs')
    body = _continuation_object(root, 'blob', blob)
    if (digest(body), len(body)) != (identity, size):
        raise ValueError('sparse-prior original source map bytes differ')
    original = json.loads(body)['sources']
    if [source for source in original if source['id'] == row.get('id')] != [row]:
        raise ValueError('sparse-prior original occurrence identity differs')
    return historical_source_bytes(root, row['path'], SPARSE_PRIOR_REVISION,
                                   SPARSE_PRIOR_PROSE[row['path']][0])


def require_next24_note_context(root):
    """Require exactly 50 original identities and the accepted current owners.

    The two reading aliases retain research-note/synthesis roles; the scope
    register retains its eight support relationships. No extra work, source
    alias or manifest form is created for the other incorporated reports.
    Original verdicts are historical evidence, not fresh execution or custody.
    """
    root = pathlib.Path(root)
    try:
        owners = json.loads(_regular_current_bytes(root,
            'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'))
        cross = json.loads(_regular_current_bytes(root,
            'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'))
        bindings = owners['historical_source_bindings']
        fields = {'path', 'repository_revision', 'git_blob', 'role', 'reading_source', 'basis'}
        if (not isinstance(bindings, list)
                or any(not isinstance(row, dict) or set(row) != fields for row in bindings)
                or len({row['path'] for row in bindings}) != len(bindings)
                or {row['path'] for row in bindings} not in
                    (set(EARLIER_FIFTY_HISTORICAL_PATHS), set(HISTORICAL_PROSE))):
            raise ValueError('the exact earlier twenty-six and next24 bindings are required')
        for n, row in NEXT24_NOTES.items():
            expected = dict(path=NEXT24_PATHS[n], repository_revision=NEXT24_REVISION,
                git_blob=row[1], role='historical-source', reading_source=row[3],
                basis='scientific-consolidation-review')
            if [binding for binding in bindings if binding['path'] == expected['path']] != [expected]:
                raise ValueError('the exact next24 original owner binding is required')
        for key, path, role in (
            ('consolidated-common-repair', 'mathematics/common-repair-and-geometric-obstructions.md', 'work-source'),
            ('consolidated-information-and-inquiry', 'mathematics/information-and-inquiry.md', 'work-source'),
            ('consolidated-objective-normativity', 'foundations/objective-normativity-and-corrective-cognition.md', 'work-source'),
            ('scientific-consolidation-review', 'docs/scientific-consolidation-review.md', 'review')):
            selected = [row for row in owners['source_additions'] if row['key'] == key]
            if len(selected) != 1:
                raise ValueError('missing or duplicate current next24 reading owner')
            admission, source = selected[0], cross['sources'][key]
            current = _regular_current_bytes(root, path)
            oid = hashlib.sha1(b'blob ' + str(len(current)).encode() + b'\0' + current).hexdigest()
            if (admission['path'] != path or source['path'] != path or admission['role'] != role
                    or admission['mode'] != '100644' or admission['git_oid'] != oid
                    or admission['bytes'] != len(current) or admission['sha256'] != digest(current)
                    or source['sha256'] != digest(current)):
                raise ValueError('current next24 scholarship or review edition differs')
            if role == 'work-source' and 'scientific-consolidation-review' not in admission['supporting_source_keys']:
                raise ValueError('current next24 work has lost its review owner')
        for n, row in NEXT24_NOTES.items():
            names = [key for key, value in cross['sources'].items() if value['path'] == NEXT24_PATHS[n]]
            if n not in NEXT24_READER_ALIASES:
                if names:
                    raise ValueError('a history-only next24 original acquired a reader alias')
                continue
            key, work, role, support, users = NEXT24_READER_ALIASES[n]
            source = cross['sources'][key]
            primary = [item for item in cross['works'] if key in item['source_keys']]
            forms = [form for item in cross['works'] for form in item.get('reading_forms', [])
                     if form.get('source') == key]
            supported = sorted(item['key'] for item in cross['works']
                               if key in item.get('supporting_source_keys', []))
            expected_form = {'source': key, 'relationship': 'historical-source'}
            if work is None:
                if primary or forms or support is not None or role is not None:
                    raise ValueError('next24 support-only original acquired a work or reading form')
            elif (len(primary) != 1 or primary[0]['key'] != work or primary[0]['role'] != role
                    or primary[0]['source_keys'] != [key] or primary[0]['reading_forms'] != [expected_form]
                    or forms != [expected_form] or primary[0]['supporting_source_keys'] != list(support)
                    or any(name not in cross['sources'] for name in support)):
                raise ValueError('next24 research-note/synthesis ownership or retained support differs')
            relation = {'from': key, 'to': row[3],
                        'kind': 'logical-content-incorporated-historical-source-retained',
                        'basis': 'scientific-consolidation-review'}
            if (names != [key] or source['sha256'] != row[0] or supported != list(users)
                    or not isinstance(source.get('read_scope'), str) or not source['read_scope'].strip()
                    or [item for item in cross['relations'] if item.get('from') == key] != [relation]
                    or any(key in journey.get('source_keys', []) for journey in cross['reader_journeys'])):
                raise ValueError('next24 source identity, support incidence or incorporation differs')
    except (KeyError, TypeError, UnicodeError) as exc:
        raise ValueError('invalid current next24 original owner bindings') from exc


def require_t4_note_context(root):
    """Require ten enumerated T4 originals and their current scholarly owners.

    Six aliases retain research-note identities; four retain support-only roles.
    The three broad source accounts are outside this admission. This validates
    a finite reading relationship, not scientific truth or permission to delete.
    """
    root = pathlib.Path(root)
    try:
        owners = json.loads(_regular_current_bytes(root,
            'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'))
        cross = json.loads(_regular_current_bytes(root,
            'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'))
        bindings = owners['historical_source_bindings']
        fields = {'path', 'repository_revision', 'git_blob', 'role', 'reading_source', 'basis'}
        if (not isinstance(bindings, list)
                or any(not isinstance(row, dict) or set(row) != fields for row in bindings)
                or len({row['path'] for row in bindings}) != len(bindings)
                or {row['path'] for row in bindings} not in
                    (set(T4_READER_HISTORICAL_PATHS), set(EARLIER_FIFTY_HISTORICAL_PATHS), set(HISTORICAL_PROSE))):
            raise ValueError('the exact T4 twenty-six or next24 fifty bindings are required')
        for key, row in T4_READER_NOTES.items():
            expected = dict(path=T4_READER_PATHS[key], repository_revision=T4_READER_REVISION,
                git_blob=row[1], role='historical-source', reading_source=row[4],
                basis='scientific-consolidation-review')
            if [binding for binding in bindings if binding['path'] == expected['path']] != [expected]:
                raise ValueError('the exact T4 historical owner binding is required')
        for key, path, role in (
            ('consolidated-information-and-inquiry', 'mathematics/information-and-inquiry.md', 'work-source'),
            ('consolidated-collective-inquiry', 'mathematics/collective-inquiry-and-strategic-coordination.md', 'work-source'),
            ('scientific-consolidation-review', 'docs/scientific-consolidation-review.md', 'review')):
            selected = [row for row in owners['source_additions'] if row['key'] == key]
            if len(selected) != 1:
                raise ValueError('missing or duplicate current T4 reading owner')
            admission, source = selected[0], cross['sources'][key]
            current = _regular_current_bytes(root, path)
            oid = hashlib.sha1(b'blob ' + str(len(current)).encode() + b'\0' + current).hexdigest()
            if (admission['path'] != path or source['path'] != path or admission['role'] != role
                    or admission['mode'] != '100644' or admission['git_oid'] != oid
                    or admission['bytes'] != len(current) or admission['sha256'] != digest(current)
                    or source['sha256'] != digest(current)):
                raise ValueError('current T4 scholarship or review edition differs')
            if role == 'work-source' and 'scientific-consolidation-review' not in admission['supporting_source_keys']:
                raise ValueError('current T4 work has lost its review owner')
        for key, row in T4_READER_NOTES.items():
            source = cross['sources'][key]
            primary = [work for work in cross['works'] if key in work['source_keys']]
            forms = [form for work in cross['works'] for form in work.get('reading_forms', [])
                     if form.get('source') == key]
            supported = sorted(work['key'] for work in cross['works']
                               if key in work.get('supporting_source_keys', []))
            expected_form = {'source': key, 'relationship': 'historical-source'}
            if row[3] is None:
                if primary or forms or row[5] is not None:
                    raise ValueError('T4 support-only original acquired a work or reading form')
            elif (len(primary) != 1 or primary[0]['key'] != row[3]
                    or primary[0]['role'] != 'research-note' or primary[0]['source_keys'] != [key]
                    or primary[0]['reading_forms'] != [expected_form] or forms != [expected_form]
                    or primary[0]['supporting_source_keys'] != list(row[5])
                    or any(support not in cross['sources'] for support in row[5])):
                raise ValueError('T4 research-note ownership or retained support differs')
            relation = {'from': key, 'to': row[4],
                        'kind': 'logical-content-incorporated-historical-source-retained',
                        'basis': 'scientific-consolidation-review'}
            if (supported != list(row[6]) or source['path'] != T4_READER_PATHS[key]
                    or source['sha256'] != row[0]
                    or not isinstance(source.get('read_scope'), str) or not source['read_scope'].strip()
                    or [name for name, item in cross['sources'].items()
                        if item['path'] == T4_READER_PATHS[key]] != [key]
                    or [r for r in cross['relations'] if r.get('from') == key] != [relation]
                    or any(key in journey.get('source_keys', []) for journey in cross['reader_journeys'])):
                raise ValueError('T4 source identity, support incidence or incorporation differs')
    except (KeyError, TypeError, UnicodeError) as exc:
        raise ValueError('invalid current T4 note owner bindings') from exc


def require_continuation_note_context(root):
    """Bind exactly four historical note readers to their incorporated science.

    The current chapters and review remain mandatory. This preserves original
    work/source ownership and support; it grants no new science, custody,
    restoration or permission to delete a note or its formal components.
    """
    root = pathlib.Path(root)
    try:
        owners = json.loads(_regular_current_bytes(root,
            'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'))
        cross = json.loads(_regular_current_bytes(root,
            'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'))
        bindings = owners['historical_source_bindings']
        fields = {'path', 'repository_revision', 'git_blob', 'role', 'reading_source', 'basis'}
        if (not isinstance(bindings, list)
                or any(not isinstance(row, dict) or set(row) != fields for row in bindings)
                or len({row['path'] for row in bindings}) != len(bindings)
                or {row['path'] for row in bindings} not in
                    (set(CONTINUATION_READER_HISTORICAL_PATHS), set(T4_READER_HISTORICAL_PATHS),
                     set(EARLIER_FIFTY_HISTORICAL_PATHS), set(HISTORICAL_PROSE))):
            raise ValueError('exact continuation sixteen or T4 twenty-six bindings are required')
        for key, row in CONTINUATION_READER_NOTES.items():
            path = CONTINUATION_READER_PATHS[key]
            expected = dict(path=path, repository_revision=CONTINUATION_READER_REVISION,
                git_blob=row[1], role='historical-source', reading_source=row[4],
                basis='scientific-consolidation-review')
            if [binding for binding in bindings if binding['path'] == path] != [expected]:
                raise ValueError('the exact continuation note owner binding is required')
        for key, path, role in (
            ('consolidated-common-repair', 'mathematics/common-repair-and-geometric-obstructions.md', 'work-source'),
            ('consolidated-information-and-inquiry', 'mathematics/information-and-inquiry.md', 'work-source'),
            ('scientific-consolidation-review', 'docs/scientific-consolidation-review.md', 'review')):
            selected = [row for row in owners['source_additions'] if row['key'] == key]
            if len(selected) != 1:
                raise ValueError('missing or duplicate current continuation reading owner')
            admission, source = selected[0], cross['sources'][key]
            current = _regular_current_bytes(root, path)
            oid = hashlib.sha1(b'blob ' + str(len(current)).encode() + b'\0' + current).hexdigest()
            if (admission['path'] != path or source['path'] != path or admission['role'] != role
                    or admission['mode'] != '100644' or admission['git_oid'] != oid
                    or admission['bytes'] != len(current) or admission['sha256'] != digest(current)
                    or source['sha256'] != digest(current)):
                raise ValueError('current continuation scholarship or review edition differs')
            if role == 'work-source' and 'scientific-consolidation-review' not in admission['supporting_source_keys']:
                raise ValueError('current continuation work has lost its review owner')
        for key, row in CONTINUATION_READER_NOTES.items():
            source = cross['sources'][key]
            works = [work for work in cross['works'] if work['key'] == row[3]]
            expected_form = {'source': key, 'relationship': 'historical-source'}
            relation = {'from': key, 'to': row[4],
                        'kind': 'logical-content-incorporated-historical-source-retained',
                        'basis': 'scientific-consolidation-review'}
            if (len(works) != 1 or works[0]['role'] != 'research-note'
                    or works[0]['source_keys'] != [key]
                    or works[0]['reading_forms'] != [expected_form]
                    or works[0]['supporting_source_keys'] != list(row[5])
                    or any(support not in cross['sources'] for support in row[5])
                    or source['path'] != CONTINUATION_READER_PATHS[key] or source['sha256'] != row[0]
                    or not isinstance(source.get('read_scope'), str) or not source['read_scope'].strip()
                    or [name for name, item in cross['sources'].items()
                        if item['path'] == CONTINUATION_READER_PATHS[key]] != [key]
                    or [work['key'] for work in cross['works'] if key in work['source_keys']] != [row[3]]
                    or [form for work in cross['works'] for form in work.get('reading_forms', [])
                        if form.get('source') == key] != [expected_form]
                    or [r for r in cross['relations'] if r.get('from') == key] != [relation]
                    or any(key in journey.get('source_keys', []) for journey in cross['reader_journeys'])):
                raise ValueError('continuation note reader identity, history or support differs')
    except (KeyError, TypeError, UnicodeError) as exc:
        raise ValueError('invalid current continuation note owner bindings') from exc


def require_fisher_context(root):
    """Bind this one Fisher source to the current inquiry chapter and review.

    This is a finite reader/source-owner contract. It does not re-prove the
    mathematics, retire the original, or qualify other incoming body links.
    """
    root = pathlib.Path(root)
    owner_path = 'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'
    cross_path = 'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'
    try:
        owners = json.loads(_regular_current_bytes(root, owner_path))
        cross = json.loads(_regular_current_bytes(root, cross_path))
        expected = dict(path=FISHER_AUDIT, repository_revision=FISHER_PROSE_REVISION,
            git_blob=HISTORICAL_PROSE[FISHER_AUDIT][0], role='historical-source',
            reading_source='consolidated-information-and-inquiry',
            basis='scientific-consolidation-review')
        bindings = [r for r in owners['historical_source_bindings'] if r['path'] == FISHER_AUDIT]
        if bindings != [expected]:
            raise ValueError('the exact Fisher source disposition is required')
        for key, path, role in (
            ('consolidated-information-and-inquiry', 'mathematics/information-and-inquiry.md', 'work-source'),
            ('scientific-consolidation-review', 'docs/scientific-consolidation-review.md', 'review')):
            selected = [r for r in owners['source_additions'] if r['key'] == key]
            if len(selected) != 1:
                raise ValueError('missing or duplicate current Fisher reading owner')
            admission, current_source = selected[0], cross['sources'][key]
            current = _regular_current_bytes(root, path)
            oid = hashlib.sha1(b'blob ' + str(len(current)).encode() + b'\0' + current).hexdigest()
            if (admission['path'] != path or current_source['path'] != path or admission['role'] != role
                    or admission['mode'] != '100644' or admission['git_oid'] != oid
                    or admission['bytes'] != len(current) or admission['sha256'] != digest(current)
                    or current_source['sha256'] != digest(current)):
                raise ValueError('current Fisher scholarship or review edition differs')
            if role == 'work-source' and 'scientific-consolidation-review' not in admission['supporting_source_keys']:
                raise ValueError('current Fisher work has lost its review owner')
        original = cross['sources']['fisher']
        forms = [f for w in cross['works'] for f in w.get('reading_forms', [])
                 if f.get('source') == 'fisher']
        relation = {'from': 'fisher', 'to': 'consolidated-information-and-inquiry',
                    'kind': 'logical-content-incorporated-historical-source-retained',
                    'basis': 'scientific-consolidation-review'}
        relations = [r for r in cross['relations'] if r.get('from') == 'fisher'
                     and r.get('kind') == relation['kind']]
        if (original['path'] != FISHER_AUDIT or original['sha256'] != HISTORICAL_PROSE[FISHER_AUDIT][1]
                or forms != [{'source': 'fisher', 'relationship': 'historical-source'}]
                or relations != [relation]
                or any('fisher' in j.get('source_keys', []) for j in cross['reader_journeys'])):
            raise ValueError('Fisher reader source is not explicitly historical-only')
        journeys = [j for j in cross['reader_journeys'] if j.get('id') == 'J06']
        if len(journeys) != 1 or journeys[0].get('source_keys') != [
                'tensor', 'coercive', 'consolidated-information-and-inquiry', 'sidecar']:
            raise ValueError('the Fisher journey must retain its exact current reading route')
    except (KeyError, TypeError, UnicodeError) as exc:
        raise ValueError('invalid current Fisher owner bindings') from exc


def _regular_current_bytes(root, path):
    target = pathlib.Path(root)
    for part in path.split('/'):
        target = target / part
        if target.is_symlink():
            raise ValueError('current reading dependency contains a symlink')
    entry = target.stat()
    if not stat.S_ISREG(entry.st_mode) or entry.st_mode & 0o111:
        raise ValueError('current reading dependency is not regular nonexecutable data')
    return target.read_bytes()


def _typed_guide_adaptation(path, original):
    replacements = TYPED_GUIDES[path][3]
    adapted = original
    for key, count in replacements.items():
        source = TYPED_SOURCE_KEYS[key]
        old = ('../../source-store/' + source.split('/source-store/', 1)[1]).encode()
        new = ('https://github.com/theislampill/orthemology/blob/' + TYPED_PROSE_REVISION + '/' + source).encode()
        if original.count(old) != count:
            raise ValueError('typed guide original link count differs')
        adapted = adapted.replace(old, new)
    return adapted


def typed_guide_source_bytes(root, path, *, allow_original=False):
    """Return one original guide after authenticating its exact link adaptation."""
    if path not in TYPED_GUIDES:
        raise ValueError('unqualified typed guide')
    blob, identity, size, replacements = TYPED_GUIDES[path]

    def git(*args):
        result = subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs', *args],
                                cwd=root, capture_output=True, check=False)
        if result.returncode:
            raise ValueError('required typed guide objects unavailable')
        return result.stdout

    expected = ('100644 blob ' + blob + '\t' + path + '\0').encode()
    if (git('cat-file', '-t', TYPED_PROSE_REVISION) != b'commit\n'
            or git('ls-tree', '-z', TYPED_PROSE_REVISION, '--', path) != expected):
        raise ValueError('typed guide original path, blob or mode differs')
    original = git('cat-file', 'blob', blob)
    actual_blob = hashlib.sha1(b'blob ' + str(len(original)).encode() + b'\0' + original).hexdigest()
    if (len(original), digest(original), actual_blob) != (size, identity, blob):
        raise ValueError('typed guide original identity differs')
    adapted = _typed_guide_adaptation(path, original)
    administrative = (administrative_guide_adaptation(path, original)
                      if path in ADMIN_GUIDES else adapted)
    current = _regular_current_bytes(root, path)
    if current not in (adapted, administrative) and not (allow_original and current == original):
        raise ValueError('typed guide is not its exact navigation adaptation')
    adapted_blob = hashlib.sha1(b'blob ' + str(len(adapted)).encode() + b'\0' + adapted).hexdigest()
    indexed = git('ls-files', '--stage', '-z', '--', path)
    choices = {('100644 ' + oid + ' 0\t' + path + '\0').encode(): body
               for oid, body in ((blob, original), (adapted_blob, adapted))}
    administrative_blob = hashlib.sha1(b'blob ' + str(len(administrative)).encode() + b'\0' + administrative).hexdigest()
    choices[('100644 ' + administrative_blob + ' 0\t' + path + '\0').encode()] = administrative
    if indexed not in choices:
        raise ValueError('typed guide index is absent, conflicted or unqualified')
    if git('cat-file', 'blob', indexed.split()[1].decode()) != choices[indexed]:
        raise ValueError('typed guide staged object differs or is unavailable')
    return original


def require_typed_context(root):
    """Bind prose history to current logic without retiring distinct evidence.

    This authenticates current owner records and bytes, not the mathematics,
    original review validity, formal replay, custody or permission to remove.
    """
    root = pathlib.Path(root)
    try:
        owners = json.loads(_regular_current_bytes(root,
            'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'))
        cross = json.loads(_regular_current_bytes(root,
            'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'))
        expected = [dict(path=path, repository_revision=TYPED_PROSE_REVISION,
            git_blob=TYPED_PROSE[path][0], role='historical-source',
            reading_source='consolidated-encodings-and-witnesses', basis='scientific-consolidation-review')
            for path in TYPED_PROSE]
        bindings = [r for r in owners['historical_source_bindings'] if r['path'] in TYPED_PROSE]
        if len(bindings) != 4 or any(bindings.count(row) != 1 for row in expected):
            raise ValueError('all four exact typed prose dispositions are required')
        for key, path, role in (
            ('consolidated-encodings-and-witnesses', 'logic/encodings-and-witnesses.md', 'work-source'),
            ('scientific-consolidation-review', 'docs/scientific-consolidation-review.md', 'review')):
            selected = [r for r in owners['source_additions'] if r['key'] == key]
            if len(selected) != 1:
                raise ValueError('missing or duplicate current typed reading owner')
            admission, source = selected[0], cross['sources'][key]
            current = _regular_current_bytes(root, path)
            oid = hashlib.sha1(b'blob ' + str(len(current)).encode() + b'\0' + current).hexdigest()
            if (admission['path'] != path or source['path'] != path or admission['role'] != role
                    or admission['mode'] != '100644' or admission['git_oid'] != oid
                    or admission['bytes'] != len(current) or admission['sha256'] != digest(current)
                    or source['sha256'] != digest(current)):
                raise ValueError('current typed scholarship or review edition differs')
            if role == 'work-source' and 'scientific-consolidation-review' not in admission['supporting_source_keys']:
                raise ValueError('current typed work has lost its review owner')
        result_ids = {
            't13-opaque': ['T13-OPAQUE-REPRESENTATION'],
            't13-residual': ['T13-RESIDUAL-HAS', 'T13-RESIDUAL-PLUS'],
            't13-bridge': ['T13-ATOM-APPLICATION-BRIDGE'],
            't14-separation': ['T14-CLOSED-PLUS-IDENTITY', 'T14-I-SKK-HAS', 'T14-I-SKK-PLUS'],
        }
        for key, path in TYPED_SOURCE_KEYS.items():
            source = cross['sources'][key]
            works = [w for w in cross['works'] if w.get('key') == key]
            if len(works) != 1:
                raise ValueError('typed original work identity is absent or duplicated')
            work = works[0]
            forms = [{'source': key, 'relationship': 'historical-source'}]
            source_keys, support = [key], []
            if key == 't14-separation':
                forms.append({'source': 't14-separation-lean', 'relationship': 'formal-component'})
                source_keys.append('t14-separation-lean')
                support = ['t14-written-review', 't14-review', 't14-suite']
            all_forms = [f for w in cross['works'] for f in w.get('reading_forms', [])
                         if f.get('source') == key]
            relation = {'from': key, 'to': 'consolidated-encodings-and-witnesses',
                        'kind': 'logical-content-incorporated-historical-source-retained',
                        'basis': 'scientific-consolidation-review'}
            relations = [r for r in cross['relations'] if r.get('from') == key
                         and r.get('kind') == relation['kind']]
            if (source['path'] != path or source['sha256'] != TYPED_PROSE[path][1]
                    or work['source_keys'] != source_keys or work['reading_forms'] != forms
                    or work['supporting_source_keys'] != support or work['existing_result_ids'] != result_ids[key]
                    or all_forms != [forms[0]] or relations != [relation]
                    or any(key in j.get('source_keys', []) for j in cross['reader_journeys'])):
                raise ValueError('typed source, current reading or retained component relationship differs')
        retained = {
            't14-separation-lean': ('48c216af205451ec75f6d761f0dbee97a0ba279dfaa386cfd125676b96d6975c', 'IntensionalIdentityTheorems.lean'),
            't14-written-review': ('996107254670edb11d47dddc03ce0b6dd4fe045ae41b6d73b2079f3c827862f1', 'Orthemology_Fourteenth_Checkpoint_Verification_v1_20261005.json'),
            't14-review': ('e9c756ef20f5eb9b5188c3d55c9808fb0462280caa8a6048182ad7b3d55c9cbb', 'Orthemology_Fourteenth_Completion_Verification_v1_20261005.json'),
        }
        for key, (identity, name) in retained.items():
            source = cross['sources'][key]
            if (source['path'] != 'experiments/orthemology-v5-successors/source-store/' + identity + '/' + name
                    or source['sha256'] != identity):
                raise ValueError('distinct typed formal or review source identity differs')
        suite = cross['sources']['t14-suite']
        if (suite['path'] != 'experiments/orthemology-v5-successors/suites/t14-identity.json'
                or suite['sha256'] != 'c71afd9b7487ee8f14a6ae9d32a4eb90f427f6ad37c69ada645665aadf731386'):
            raise ValueError('distinct typed suite identity differs')
        for path in TYPED_GUIDES:
            typed_guide_source_bytes(root, path)
    except (KeyError, TypeError, UnicodeError) as error:
        raise ValueError('malformed typed current-owner contract') from error


def mediator_guide_source_bytes(root, *, allow_original=False):
    """Keep the original guide identity and admit exactly three pinned links.

    The guide must remain physically present. This is a finite navigation
    adaptation, never another prose absence or an unbounded source fallback.
    """
    root = pathlib.Path(root)
    def git(*args):
        result = subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs', *args],
                                cwd=root, capture_output=True, check=False)
        if result.returncode:
            raise ValueError('required guide Git objects unavailable')
        return result.stdout
    expected = ('100644 blob ' + MEDIATOR_GUIDE_BLOB + '\t' + MEDIATOR_GUIDE + '\0').encode()
    if git('cat-file', '-t', MEDIATOR_PROSE_REVISION) != b'commit\n' or git(
            'ls-tree', '-z', MEDIATOR_PROSE_REVISION, '--', MEDIATOR_GUIDE) != expected:
        raise ValueError('original guide revision/path/blob/mode differs')
    original = git('cat-file', 'blob', MEDIATOR_GUIDE_BLOB)
    if (len(original), digest(original)) != (MEDIATOR_GUIDE_BYTES, MEDIATOR_GUIDE_SHA256):
        raise ValueError('original guide identity differs')
    old = ('../../source-store/' + MEDIATOR_COORDINATION.split('/source-store/', 1)[1]).encode()
    new = ('https://github.com/theislampill/orthemology/blob/' + MEDIATOR_PROSE_REVISION +
           '/' + MEDIATOR_COORDINATION).encode()
    if original.count(old) != 3:
        raise ValueError('original guide does not contain its three bound links')
    adapted = original.replace(old, new)
    current = _regular_current_bytes(root, MEDIATOR_GUIDE)
    if current != adapted and not (allow_original and current == original):
        raise ValueError('guide is not the exact three-link navigation adaptation')
    adapted_blob = hashlib.sha1(b'blob ' + str(len(adapted)).encode() + b'\0' + adapted).hexdigest()
    indexed = git('ls-files', '--stage', '-z', '--', MEDIATOR_GUIDE)
    choices = {('100644 ' + blob + ' 0\t' + MEDIATOR_GUIDE + '\0').encode(): data
               for blob, data in ((MEDIATOR_GUIDE_BLOB, original), (adapted_blob, adapted))}
    if indexed not in choices:
        raise ValueError('guide index is absent, conflicted or has an unqualified edition/mode')
    indexed_blob = indexed.split()[1].decode()
    if git('cat-file', 'blob', indexed_blob) != choices[indexed]:
        raise ValueError('guide staged object is unavailable or differs')
    return original


def require_mediator_context(root):
    """Require the existing current scholarship, review and explicit source roles."""
    root = pathlib.Path(root)
    owner_path = 'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'
    cross_path = 'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'
    try:
        owners = json.loads(_regular_current_bytes(root, owner_path))
        cross = json.loads(_regular_current_bytes(root, cross_path))
        expected_bindings = [dict(path=path, repository_revision=MEDIATOR_PROSE_REVISION,
            git_blob=MEDIATOR_PROSE[path][0], role='historical-source',
            reading_source='consolidated-collective-inquiry', basis='scientific-consolidation-review')
            for path in MEDIATOR_PROSE]
        bindings = [r for r in owners['historical_source_bindings'] if r['path'] in MEDIATOR_PROSE]
        if len(bindings) != 2 or any(bindings.count(row) != 1 for row in expected_bindings):
            raise ValueError('both exact mediator source dispositions are required')
        for key, path, role in (
            ('consolidated-collective-inquiry', 'mathematics/collective-inquiry-and-strategic-coordination.md', 'work-source'),
            ('scientific-consolidation-review', 'docs/scientific-consolidation-review.md', 'review')):
            selected = [r for r in owners['source_additions'] if r['key'] == key]
            if len(selected) != 1:
                raise ValueError('missing or duplicate current mediator reading owner')
            admission, source = selected[0], cross['sources'][key]
            current = _regular_current_bytes(root, path)
            oid = hashlib.sha1(b'blob ' + str(len(current)).encode() + b'\0' + current).hexdigest()
            if (admission['path'] != path or source['path'] != path or admission['role'] != role
                    or admission['mode'] != '100644' or admission['git_oid'] != oid
                    or admission['bytes'] != len(current) or admission['sha256'] != digest(current)
                    or source['sha256'] != digest(current)):
                raise ValueError('current mediator scholarship or review edition differs')
            if role == 'work-source' and 'scientific-consolidation-review' not in admission['supporting_source_keys']:
                raise ValueError('current mediator work has lost its review owner')
        for key, path in (('coordination', MEDIATOR_COORDINATION),
                          ('t20-c03-6d8c1b108c74df46', MEDIATOR_APPROXIMATION)):
            source = cross['sources'][key]
            forms = [f for w in cross['works'] for f in w.get('reading_forms', []) if f.get('source') == key]
            relation = {'from': key, 'to': 'consolidated-collective-inquiry',
                        'kind': 'logical-content-incorporated-historical-source-retained',
                        'basis': 'scientific-consolidation-review'}
            relations = [r for r in cross['relations'] if r.get('from') == key and r.get('kind') == relation['kind']]
            if (source['path'] != path or source['sha256'] != MEDIATOR_PROSE[path][1]
                    or forms != [{'source': key, 'relationship': 'historical-source'}]
                    or relations != [relation]
                    or any(key in j.get('source_keys', []) for j in cross['reader_journeys'])):
                raise ValueError('mediator source has lost its exact current reading relationship')
        mediator_guide_source_bytes(root)
    except (KeyError, TypeError, UnicodeError) as error:
        raise ValueError('malformed mediator current-owner contract') from error


def _require_self_contained_index_v2(body):
    """Accept the bounded SHA-1 v2 format without shared or opaque dependencies."""
    end = len(body) - 20
    if (end < 12 or body[:4] != b'DIRC'
            or struct.unpack('>I', body[4:8])[0] != 2
            or hashlib.sha1(body[:end]).digest() != body[end:]):
        raise ValueError('unsupported index format')
    count = struct.unpack('>I', body[8:12])[0]
    offset = 12
    if count > (end - offset) // 64:
        raise ValueError('invalid index entry count')
    for _ in range(count):
        start = offset
        if offset + 62 > end:
            raise ValueError('truncated index entry')
        flags = struct.unpack('>H', body[offset + 60:offset + 62])[0]
        name = offset + 62
        stop = body.find(b'\0', name, end)
        if (flags & 0x4000 or stop <= name
                or (flags & 0xFFF) != min(stop - name, 0xFFF)):
            raise ValueError('unsupported index entry')
        offset = start + ((stop + 1 - start + 7) // 8) * 8
        if offset > end or any(body[stop:offset]):
            raise ValueError('invalid index padding')
    while offset < end:
        if offset + 8 > end:
            raise ValueError('truncated index extension')
        signature = body[offset:offset + 4]
        size = struct.unpack('>I', body[offset + 4:offset + 8])[0]
        # No split-index link, sparse index, monitor/cache dependency, or
        # unknown extension is interpreted or silently rebuilt here.
        if signature not in {b'TREE', b'REUC', b'EOIE', b'IEOT'}:
            raise ValueError('unsupported index dependency')
        offset += 8 + size
        if offset > end:
            raise ValueError('truncated index extension payload')


def readonly_git_diff(root, command):
    """Run an existing diff against an exact private index, preserving its mtime.

    Git's normal stat-only filtering remains enabled. Any refresh is confined
    to the disposable copy. Unsupported inputs return an unavailable comparison;
    the active index is never rewritten or restored by this helper.
    """
    command = list(command)

    def unavailable():
        return subprocess.CompletedProcess(command, 128, b'',
                                           b'read-only index comparison unavailable')

    def query(*args):
        return subprocess.run(['git', '--no-replace-objects', *args],
                              cwd=root, capture_output=True, check=False)

    def state(info):
        return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
                info.st_mtime_ns, info.st_ctime_ns)

    if command[:2] != ['git', 'diff'] and command[:3] != ['git', '--no-replace-objects', 'diff']:
        return unavailable()
    try:
        split = query('config', '--type=bool', '--get', 'core.splitIndex')
        if not ((split.returncode == 1 and not split.stdout)
                or (split.returncode == 0 and split.stdout == b'false\n')):
            return unavailable()
        algorithm = query('rev-parse', '--show-object-format=storage')
        location = query('rev-parse', '--path-format=absolute', '--git-path', 'index')
        if algorithm.returncode or algorithm.stdout != b'sha1\n' or location.returncode:
            return unavailable()
        active = pathlib.Path(os.fsdecode(location.stdout.removesuffix(b'\n')))
        if not active.is_absolute():
            return unavailable()
        initial = active.lstat()
        if not stat.S_ISREG(initial.st_mode):
            return unavailable()
        with active.open('rb') as source:
            if state(os.fstat(source.fileno())) != state(initial):
                return unavailable()
            body = source.read()
            if len(body) != initial.st_size or state(active.lstat()) != state(initial):
                return unavailable()
            _require_self_contained_index_v2(body)
            with tempfile.TemporaryDirectory(prefix='readonly-git-index-') as directory:
                shadow = pathlib.Path(directory) / 'index'
                shadow.write_bytes(body)
                shadow.chmod(0o600)
                os.utime(shadow, ns=(initial.st_atime_ns, initial.st_mtime_ns))
                if shadow.read_bytes() != body or shadow.stat().st_mtime_ns != initial.st_mtime_ns:
                    return unavailable()
                env = dict(os.environ, GIT_INDEX_FILE=str(shadow))
                result = subprocess.run(command, cwd=root, env=env,
                                        capture_output=True, check=False)
            source.seek(0)
            if (state(active.lstat()) != state(initial)
                    or state(os.fstat(source.fileno())) != state(initial)
                    or source.read() != body):
                return unavailable()
            return result
    except (OSError, ValueError):
        return unavailable()


def digest(body):
    return hashlib.sha256(body).hexdigest()


# Exact formal aliases retain full arguments, witnesses, false controls,
# licenses and original logical module coordinates. Source acquisition and
# staging confer no fresh Lean result, historical replay or research adoption.

# Exact current destinations; the original71 source/proof identities stay below.
FORMAL_CURRENT_PROVIDERS = (('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/CertificateFrontier.lean',
  'formal/certificate-frontier/CertificateFrontier.lean'),
 ('research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/Controls.lean',
  'formal/certificate-frontier/Controls.lean'),
 ('research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/independent-review/ScopeChecks.lean',
  'formal/certificate-frontier/ScopeChecks.lean'),
 ('research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/CostBlind.lean',
  'formal/certificate-frontier/mutations/CostBlind.lean'),
 ('research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/CurrentCost.lean',
  'formal/certificate-frontier/mutations/CurrentCost.lean'),
 ('research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/InfinitePrice.lean',
  'formal/certificate-frontier/mutations/InfinitePrice.lean'))
FORMAL_CURRENT_PROVIDERS_SHA256 = 'e1e7f0842bba4e09d1a4008e9b2a17029fd329b9414f6360695d5091fe98852a'
FORMAL_PROVIDER_PATHS = frozenset(canonical for canonical, _ in FORMAL_CURRENT_PROVIDERS)

FORMAL_COPY_MEMBERS = (('experiments/orthemology-v5-continuations/source-store/0f8e551de28b6bdf549e0d2ecba0932bb2758b8ff57aaf5f1cf5956d7d88d8cd.lean',
  'experiments/orthemology-v5/source/lean/GeneratedExamples.lean',
  'e28a54b251fb81375367099fdcff50f182c2692e',
  '0f8e551de28b6bdf549e0d2ecba0932bb2758b8ff57aaf5f1cf5956d7d88d8cd',
  13685),
 ('experiments/orthemology-v5-continuations/source-store/12dfbed26b887067f2bbd2a75930d038558b3a5c715100d7c25d3cfee79a7fdb.lean',
  'experiments/orthemology-v5/source/lean/RelationalFragment.lean',
  '74220a92cbf0c072e42402bd0a41d2597e4bdb90',
  '12dfbed26b887067f2bbd2a75930d038558b3a5c715100d7c25d3cfee79a7fdb',
  6417),
 ('experiments/orthemology-v5-continuations/source-store/4c1d8a9d8a9a6ebec9f5e1a1ee41008b75fbfffeabbbd9ee489ea21982425a08.lean',
  'experiments/orthemology-v5/source/lean/HurkensBoundary.lean',
  '074187709780bc0e313ac5ddec5cf4625a9a233d',
  '4c1d8a9d8a9a6ebec9f5e1a1ee41008b75fbfffeabbbd9ee489ea21982425a08',
  2245),
 ('experiments/orthemology-v5-continuations/source-store/766ae9391263f193c6e84e16042281fb5e70fe680f083f0359b4b3c10f215779.lean',
  'experiments/orthemology-v5/source/lean/OperationalKernel.lean',
  'ad434829b298fb58e95aa64a8b8edb3b219e6b21',
  '766ae9391263f193c6e84e16042281fb5e70fe680f083f0359b4b3c10f215779',
  8778),
 ('experiments/orthemology-v5-continuations/source-store/8485a2156b943ce569af6f219d69d7d24b00b41b04b8225a68d7480d2d70522d.lean',
  'experiments/orthemology-v5/source/lean/AlmostSureBoundary.lean',
  'be13b34a2d1ba2d8a846cc7a279ae55fb1283fbf',
  '8485a2156b943ce569af6f219d69d7d24b00b41b04b8225a68d7480d2d70522d',
  3234),
 ('experiments/orthemology-v5-successors/source-store/b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183/PhaseStabilization.lean',
  'experiments/orthemology-v5-continuations/source-store/b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183.lean',
  'bf40cccf2a6c791714ce4abf9f39ab2532c0e99e',
  'b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183',
  4741),
 ('experiments/orthemology-v5-continuations/source-store/d3494436356f8aec5510b004e2a977c9946533f6190219f30eee2de511b53f4e.lean',
  'experiments/orthemology-v5/source/lean/OperationalBoundary.lean',
  'ffa0b6d903b3285a3282b056f7df3c9de6770ebe',
  'd3494436356f8aec5510b004e2a977c9946533f6190219f30eee2de511b53f4e',
  2599),
 ('experiments/orthemology-v5-successors/source-store/f3e08557b57a745bae547dc827755616cd6c6824bf1360441a72789036e1cd96/AuditSupport.lean',
  'experiments/orthemology-v5/source/lean/AuditSupport.lean',
  '4ba3d9db5e9157c7c183a1045d82e3c40be887f9',
  'f3e08557b57a745bae547dc827755616cd6c6824bf1360441a72789036e1cd96',
  1024),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/inherited/OriginalBearerBridge.lean',
  'experiments/orthemology-v5-successors/source-store/086fb3bb7d7cd152b19ee2e6af47c25b92bd5b7825b0bfb9ee16a9ef7a56ba99/OriginalBearerBridge.lean',
  '7b8effb1f2281515208dcb23171d2bc7a004c97f',
  '086fb3bb7d7cd152b19ee2e6af47c25b92bd5b7825b0bfb9ee16a9ef7a56ba99',
  6940),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/review/replay/inherited/OriginalBearerBridge.lean',
  'experiments/orthemology-v5-successors/source-store/086fb3bb7d7cd152b19ee2e6af47c25b92bd5b7825b0bfb9ee16a9ef7a56ba99/OriginalBearerBridge.lean',
  '7b8effb1f2281515208dcb23171d2bc7a004c97f',
  '086fb3bb7d7cd152b19ee2e6af47c25b92bd5b7825b0bfb9ee16a9ef7a56ba99',
  6940),
 ('research/t20-live-20261009/checkpoints/CP08/recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/sources/original-bearer-bridge/OriginalBearerBridge.lean',
  'experiments/orthemology-v5-successors/source-store/086fb3bb7d7cd152b19ee2e6af47c25b92bd5b7825b0bfb9ee16a9ef7a56ba99/OriginalBearerBridge.lean',
  '7b8effb1f2281515208dcb23171d2bc7a004c97f',
  '086fb3bb7d7cd152b19ee2e6af47c25b92bd5b7825b0bfb9ee16a9ef7a56ba99',
  6940),
 ('experiments/orthemology-v5-successors/source-store/0e0636bf2cbd583b0a7193d9cc5985bdca6c5e52a0c895f01e9cd71b5677e34c/ReviewerReadback.lean',
  'experiments/orthemology-v5-successors/source-store/0e0636bf2cbd583b0a7193d9cc5985bdca6c5e52a0c895f01e9cd71b5677e34c/ReadbackAudit.lean',
  '25cafa10bad0bc925fd900e8ccd18ad85c4cdd51',
  '0e0636bf2cbd583b0a7193d9cc5985bdca6c5e52a0c895f01e9cd71b5677e34c',
  4035),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/inherited/SourceIdentityDerived.lean',
  'experiments/orthemology-v5-successors/source-store/51b8a964e5854cd383afd5a862554126d4f8ebcf4a301e435ef795ac2c5cbb54/SourceIdentityDerived.lean',
  '1ae461afa51ba4f339fa02b154b6ec781407d968',
  '51b8a964e5854cd383afd5a862554126d4f8ebcf4a301e435ef795ac2c5cbb54',
  7438),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/review/replay/inherited/SourceIdentityDerived.lean',
  'experiments/orthemology-v5-successors/source-store/51b8a964e5854cd383afd5a862554126d4f8ebcf4a301e435ef795ac2c5cbb54/SourceIdentityDerived.lean',
  '1ae461afa51ba4f339fa02b154b6ec781407d968',
  '51b8a964e5854cd383afd5a862554126d4f8ebcf4a301e435ef795ac2c5cbb54',
  7438),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/inherited/BridgeControls.lean',
  'experiments/orthemology-v5-successors/source-store/be1ba7d32e603bc2c4d725d9fc0425150b992aa24e0cab8c9a7807fcd36371a8/BridgeControls.lean',
  '272f4f1ffb8c78a0e74033edf86bbfb928f3f9ff',
  'be1ba7d32e603bc2c4d725d9fc0425150b992aa24e0cab8c9a7807fcd36371a8',
  9487),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/review/replay/inherited/BridgeControls.lean',
  'experiments/orthemology-v5-successors/source-store/be1ba7d32e603bc2c4d725d9fc0425150b992aa24e0cab8c9a7807fcd36371a8/BridgeControls.lean',
  '272f4f1ffb8c78a0e74033edf86bbfb928f3f9ff',
  'be1ba7d32e603bc2c4d725d9fc0425150b992aa24e0cab8c9a7807fcd36371a8',
  9487),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification-review/frozen/CalibratedPanels.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification/CalibratedPanels.lean',
  '89edc9114951ee0752e6baf3309692d6c15eb029',
  '1f96630cac12107b21c96615a14cc817d16af4d29264c47a742bd2da59c2382a',
  3454),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/formal-identification/CalibratedPanels.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification/CalibratedPanels.lean',
  '89edc9114951ee0752e6baf3309692d6c15eb029',
  '1f96630cac12107b21c96615a14cc817d16af4d29264c47a742bd2da59c2382a',
  3454),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification-review/frozen/Calibration.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification/Calibration.lean',
  '8b0d2c9b22c36140a4b7249fbd59509c0d3e1bf2',
  'e5b126e3b9e9cdb8805f3417d90d3431611ec86a83614a925d5671b2dc10aeba',
  5422),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification-review/mutation-controls/CalibrationControl.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification/Calibration.lean',
  '8b0d2c9b22c36140a4b7249fbd59509c0d3e1bf2',
  'e5b126e3b9e9cdb8805f3417d90d3431611ec86a83614a925d5671b2dc10aeba',
  5422),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/formal-identification/Calibration.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification/Calibration.lean',
  '8b0d2c9b22c36140a4b7249fbd59509c0d3e1bf2',
  'e5b126e3b9e9cdb8805f3417d90d3431611ec86a83614a925d5671b2dc10aeba',
  5422),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification-review/frozen/HitTransform.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification/HitTransform.lean',
  'a50b0fd5b8bc0d0bf44e2ebb2a1548b573b97f28',
  '046c5be8de2e0878ce3820860b26cd43b9199de52c82dd22f647ee471f56b3d7',
  6036),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification-review/mutation-controls/HitTransformControl.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification/HitTransform.lean',
  'a50b0fd5b8bc0d0bf44e2ebb2a1548b573b97f28',
  '046c5be8de2e0878ce3820860b26cd43b9199de52c82dd22f647ee471f56b3d7',
  6036),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/formal-identification/HitTransform.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification/HitTransform.lean',
  'a50b0fd5b8bc0d0bf44e2ebb2a1548b573b97f28',
  '046c5be8de2e0878ce3820860b26cd43b9199de52c82dd22f647ee471f56b3d7',
  6036),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification-review/frozen/Verification.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification/Verification.lean',
  'ef1086b283a133bce96792cfe898fcf14ede26ff',
  '1b5d16d632df462189d2a510d96b3ea662e8b166879a8c44825905d0509b7e68',
  993),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/frozen/BernoulliAssignments.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/BernoulliAssignments.lean',
  'b124aa9bf8f261d042bc7fe591103a0b5ce13aea',
  'e6dd1e4814bb0bb6c977cd3b6e4ee600e8d4cdfeb5c4564148d3bb5a38eb8eba',
  2636),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/mutation-workspace/BernoulliAssignments.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/BernoulliAssignments.lean',
  'b124aa9bf8f261d042bc7fe591103a0b5ce13aea',
  'e6dd1e4814bb0bb6c977cd3b6e4ee600e8d4cdfeb5c4564148d3bb5a38eb8eba',
  2636),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/review/replay/BernoulliAssignments.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/BernoulliAssignments.lean',
  'b124aa9bf8f261d042bc7fe591103a0b5ce13aea',
  'e6dd1e4814bb0bb6c977cd3b6e4ee600e8d4cdfeb5c4564148d3bb5a38eb8eba',
  2636),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/frozen/EndpointLaw.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/EndpointLaw.lean',
  '2a3a51280a0b15f12f0e54c8a03052d3863da912',
  '0a1e6aa470334ecb7766d53bbdd984b2cdeab0945ec3639984c66d4f3980f616',
  2704),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/mutation-workspace/EndpointLaw.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/EndpointLaw.lean',
  '2a3a51280a0b15f12f0e54c8a03052d3863da912',
  '0a1e6aa470334ecb7766d53bbdd984b2cdeab0945ec3639984c66d4f3980f616',
  2704),
 ('research/t20-live-20261009/checkpoints/CP03/t20-next-frontier-20261008/formal-route-probability/EndpointLaw.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/EndpointLaw.lean',
  '2a3a51280a0b15f12f0e54c8a03052d3863da912',
  '0a1e6aa470334ecb7766d53bbdd984b2cdeab0945ec3639984c66d4f3980f616',
  2704),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/review/replay/EndpointLaw.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/EndpointLaw.lean',
  '2a3a51280a0b15f12f0e54c8a03052d3863da912',
  '0a1e6aa470334ecb7766d53bbdd984b2cdeab0945ec3639984c66d4f3980f616',
  2704),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/frozen/GenerativePanels.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/GenerativePanels.lean',
  '130bc2ea400b43bbbf09c79c31651904b1053e16',
  '086ec54ea878df015b5a533c77d8b93fc440cad9b68c68e349388bbd376581e9',
  4484),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/mutation-workspace/GenerativePanels.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/GenerativePanels.lean',
  '130bc2ea400b43bbbf09c79c31651904b1053e16',
  '086ec54ea878df015b5a533c77d8b93fc440cad9b68c68e349388bbd376581e9',
  4484),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/review/replay/GenerativePanels.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/GenerativePanels.lean',
  '130bc2ea400b43bbbf09c79c31651904b1053e16',
  '086ec54ea878df015b5a533c77d8b93fc440cad9b68c68e349388bbd376581e9',
  4484),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/frozen/HistogramGrouping.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/HistogramGrouping.lean',
  'd3c9ebb18b555926ccea4ed12b637a04e4340454',
  '07de3ab146e22f88555edf16cafd96cb1fd7547935f640f64c790861ceed42dc',
  2601),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/mutation-workspace/HistogramGrouping.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/HistogramGrouping.lean',
  'd3c9ebb18b555926ccea4ed12b637a04e4340454',
  '07de3ab146e22f88555edf16cafd96cb1fd7547935f640f64c790861ceed42dc',
  2601),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/review/replay/HistogramGrouping.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/HistogramGrouping.lean',
  'd3c9ebb18b555926ccea4ed12b637a04e4340454',
  '07de3ab146e22f88555edf16cafd96cb1fd7547935f640f64c790861ceed42dc',
  2601),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/frozen/Model.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/Model.lean',
  '76aceddb4d47731c1db7319720c2e503cd117f1b',
  '878e4e82b13cb572f8d5ce838c10efd930acb35cfdd2b44915c22bb19980769e',
  3042),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/mutation-workspace/Model.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/Model.lean',
  '76aceddb4d47731c1db7319720c2e503cd117f1b',
  '878e4e82b13cb572f8d5ce838c10efd930acb35cfdd2b44915c22bb19980769e',
  3042),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/review/replay/Model.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/Model.lean',
  '76aceddb4d47731c1db7319720c2e503cd117f1b',
  '878e4e82b13cb572f8d5ce838c10efd930acb35cfdd2b44915c22bb19980769e',
  3042),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/frozen/Verification.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/Verification.lean',
  'b4679342ad203cdee85eeec726ab44459dfc4fed',
  'c66cda0da6393d46178c07912016e02a73d23bdae123fb38a5513ae4fbf57e7d',
  1548),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/mutation-workspace/Verification.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/Verification.lean',
  'b4679342ad203cdee85eeec726ab44459dfc4fed',
  'c66cda0da6393d46178c07912016e02a73d23bdae123fb38a5513ae4fbf57e7d',
  1548),
 ('research/t20-live-20261009/checkpoints/CP03/t20-next-frontier-20261008/formal-route-probability/Verification.lean',
  'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability/Verification.lean',
  'b4679342ad203cdee85eeec726ab44459dfc4fed',
  'c66cda0da6393d46178c07912016e02a73d23bdae123fb38a5513ae4fbf57e7d',
  1548),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/review/replay/ScopeTest.lean',
  'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/ScopeTest.lean',
  '2e633f3980f6db1638934f099089efd335bed4a1',
  'a53b58e88b6b3f7a9dd4b6693a223743e766b96bfc675e59086cb26d277b9d30',
  5595),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/review/replay/results/fixed_act_token.lean',
  'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/results/fixed_act_token.lean',
  '88934485195bb34029f82283ead3269c52a23e55',
  '1802cfb96c76e1202e0812e088313676441d946dfce4a6670e93e0aa88dfd64b',
  243),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/review/replay/results/necessary_target.lean',
  'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/results/necessary_target.lean',
  '0e157feea11945f8dc94b48e79dad166a0ce33dc',
  'a4ffbd3832735b5fafd1b50ebba14c280abd5ba7039adcf1d6cc4edc12488852',
  261),
 ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/review/replay/results/normalization_forces_nonempty_endpoint.lean',
  'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/productive-sufficiency-scope/results/normalization_forces_nonempty_endpoint.lean',
  '141798d17996aaaf4cc7fb8067e7a861ea28b145',
  'b56be9cad3c7c7caba544a31647ee224af15a190c4bc7bc87c3a6e80253575de',
  266),
 ('research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate-review/ImportInventory.lean',
  'research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate/ImportInventory.lean',
  'da869ba63fddd5c5c783405d923b4b2815848dfe',
  '240941371ef58576258cd8b879ab2d6119157d95e3b0f11156d027585fea0620',
  194),
 ('research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate-review/kernel-isolated/FalseConnectorPremise.lean',
  'research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate/kernel-replay/FalseConnectorPremise.lean',
  '464f2de70988a7030f70d09db2cd232d05558322',
  '58f1e282f69df4c355264695de926ecb0942a9126b00f34dca66b5253e7f32d6',
  3263),
 ('research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate-review/kernel-isolated/FalseCountBound.lean',
  'research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate/kernel-replay/FalseCountBound.lean',
  '1d690c1addabec5fa8fd7f88f2af0aaabb412b9a',
  '3fdd60e121af0abade18bdb59331ac4f8be8e9eeee8b3490bbebb1895396518f',
  3277),
 ('research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate-review/kernel-isolated/RetainedInterior.lean',
  'research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate/RetainedInterior.lean',
  '5a3c1979a61ec161a21d02a6ebbf6106981c366e',
  '85a487cd9041cc46d319a7f239ba77f911293eb922ca8dc9f97e60e98cbc170a',
  3269),
 ('research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate/kernel-replay/RetainedInterior.lean',
  'research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate/RetainedInterior.lean',
  '5a3c1979a61ec161a21d02a6ebbf6106981c366e',
  '85a487cd9041cc46d319a7f239ba77f911293eb922ca8dc9f97e60e98cbc170a',
  3269),
 ('research/t20-live-20261009/checkpoints/CP19/graph-constrained-continuation-20261009/verified/GraphContinuation.lean',
  'research/t20-live-20261009/checkpoints/CP19/graph-constrained-continuation-20261009/GraphContinuation.lean',
  '8ad376afef34fed1a36a06756c333e845c957f65',
  '2f8b4df91a832fb3d656ee9d854b7a5d625236ecc127588bc574d051c4b2cf73',
  10145),
 ('research/t20-live-20261009/checkpoints/CP19/graph-continuation-review-20261009/lean-replay/GraphContinuation.lean',
  'research/t20-live-20261009/checkpoints/CP19/graph-constrained-continuation-20261009/GraphContinuation.lean',
  '8ad376afef34fed1a36a06756c333e845c957f65',
  '2f8b4df91a832fb3d656ee9d854b7a5d625236ecc127588bc574d051c4b2cf73',
  10145),
 ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/frontier-kernel-replay/CertificateFrontier.lean',
  'research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/CertificateFrontier.lean',
  '208cf6e6250c6ff50d0b03575a6ae7926b70d1ed',
  '5e799995b95e37105dff8dfe10e5ba78dfe44034334353bcf66107069e8a67e0',
  12278),
 ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/independent-review/CertificateFrontier.lean',
  'research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/CertificateFrontier.lean',
  '208cf6e6250c6ff50d0b03575a6ae7926b70d1ed',
  '5e799995b95e37105dff8dfe10e5ba78dfe44034334353bcf66107069e8a67e0',
  12278),
 ('research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/CertificateFrontier.lean',
  'research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/CertificateFrontier.lean',
  '208cf6e6250c6ff50d0b03575a6ae7926b70d1ed',
  '5e799995b95e37105dff8dfe10e5ba78dfe44034334353bcf66107069e8a67e0',
  12278),
 ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/frontier-kernel-replay/Controls.lean',
  'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/Controls.lean',
  '1c6b8900e600c63e30f0aa83f49f7db8211a7cdf',
  '7d49f0df7d1b5eb633e6edebf17bc0a967eeff1718b9e1cc3fcab1513afb5132',
  2410),
 ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/Controls.lean',
  'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/Controls.lean',
  '1c6b8900e600c63e30f0aa83f49f7db8211a7cdf',
  '7d49f0df7d1b5eb633e6edebf17bc0a967eeff1718b9e1cc3fcab1513afb5132',
  2410),
 ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/independent-review/Controls.lean',
  'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/Controls.lean',
  '1c6b8900e600c63e30f0aa83f49f7db8211a7cdf',
  '7d49f0df7d1b5eb633e6edebf17bc0a967eeff1718b9e1cc3fcab1513afb5132',
  2410),
 ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/frontier-kernel-replay/mutations/CostBlind.lean',
  'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/CostBlind.lean',
  '01cef9257fc16b90c16ae14ca9e65aef41cdd787',
  'c05bf6d3207aeeaa7dddc222092c73d44f73ecc5eab5c8d465485a9a540d5776',
  227),
 ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/independent-review/mutations/CostBlind.lean',
  'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/CostBlind.lean',
  '01cef9257fc16b90c16ae14ca9e65aef41cdd787',
  'c05bf6d3207aeeaa7dddc222092c73d44f73ecc5eab5c8d465485a9a540d5776',
  227),
 ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/mutations/CostBlind.lean',
  'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/CostBlind.lean',
  '01cef9257fc16b90c16ae14ca9e65aef41cdd787',
  'c05bf6d3207aeeaa7dddc222092c73d44f73ecc5eab5c8d465485a9a540d5776',
  227),
 ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/frontier-kernel-replay/mutations/CurrentCost.lean',
  'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/CurrentCost.lean',
  '9ad7316c3906603cd262cb781736078b18cd14a5',
  '876039d480a1415531f1f099679c5094327caf35c7933a36550e09692de1e83d',
  249),
 ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/independent-review/mutations/CurrentCost.lean',
  'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/CurrentCost.lean',
  '9ad7316c3906603cd262cb781736078b18cd14a5',
  '876039d480a1415531f1f099679c5094327caf35c7933a36550e09692de1e83d',
  249),
 ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/mutations/CurrentCost.lean',
  'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/CurrentCost.lean',
  '9ad7316c3906603cd262cb781736078b18cd14a5',
  '876039d480a1415531f1f099679c5094327caf35c7933a36550e09692de1e83d',
  249),
 ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/frontier-kernel-replay/mutations/InfinitePrice.lean',
  'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/InfinitePrice.lean',
  'ffa13821c157cd943b1bcb5f6aa514c917f198b1',
  '0b2d8b2584f48d343d753a373161e28f93c397982ce9ab4c098b8daf16db31fe',
  293),
 ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/independent-review/mutations/InfinitePrice.lean',
  'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/InfinitePrice.lean',
  'ffa13821c157cd943b1bcb5f6aa514c917f198b1',
  '0b2d8b2584f48d343d753a373161e28f93c397982ce9ab4c098b8daf16db31fe',
  293),
 ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/mutations/InfinitePrice.lean',
  'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/InfinitePrice.lean',
  'ffa13821c157cd943b1bcb5f6aa514c917f198b1',
  '0b2d8b2584f48d343d753a373161e28f93c397982ce9ab4c098b8daf16db31fe',
  293),
 ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/independent-review/ScopeChecks.lean',
  'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/independent-review/ScopeChecks.lean',
  '2efba39e95c7b0cf38b246654d64f16e099f8e31',
  '6218ff6fa7b6e5b304859c2f4ad3d512118f1a3c9b68ec7e446d6cc1cd2d78a6',
  1345))
FORMAL_COPY_MEMBERS_SHA256 = 'de1c51c3a3f27aa190d8237c91fe68ccbb21154b17c3721a489fe71d6ff59d37'
FORMAL_PUBLIC_MEMBERS = (('experiments/orthemology-v5-continuations/source-store/0f8e551de28b6bdf549e0d2ecba0932bb2758b8ff57aaf5f1cf5956d7d88d8cd.lean',
  'e226857f99c81c90bacf27580cf44f80efee8cd8b51105642a98709be04e6230'),
 ('experiments/orthemology-v5-continuations/source-store/12dfbed26b887067f2bbd2a75930d038558b3a5c715100d7c25d3cfee79a7fdb.lean',
  'b39c06d649dea07629d6870530139a1b73137a0334f7544203fdb27c203f1169'),
 ('experiments/orthemology-v5-continuations/source-store/4c1d8a9d8a9a6ebec9f5e1a1ee41008b75fbfffeabbbd9ee489ea21982425a08.lean',
  '2bc085f620d469552b5ff7e483b59eede21db78506973d046ef83db1882c3206'),
 ('experiments/orthemology-v5-continuations/source-store/766ae9391263f193c6e84e16042281fb5e70fe680f083f0359b4b3c10f215779.lean',
  '203b8cf11d60fbf245c0355b5f132757ac68c49d56ec81a0b36650e10425c73b'),
 ('experiments/orthemology-v5-continuations/source-store/8485a2156b943ce569af6f219d69d7d24b00b41b04b8225a68d7480d2d70522d.lean',
  'babb169a57c56df564fd57ab434718f4909e8f5bd24d63dc639ac47a1f37bac2'),
 ('experiments/orthemology-v5-continuations/source-store/d3494436356f8aec5510b004e2a977c9946533f6190219f30eee2de511b53f4e.lean',
  '297f8bede968c500077567a69a9f7ba3c92629aced150d6a32bfdd80c6bbae76'),
 ('experiments/orthemology-v5-continuations/source-store/f3e08557b57a745bae547dc827755616cd6c6824bf1360441a72789036e1cd96.lean',
  '82ee275d73c1175828246e22558d55b0f536f9796cedf209760114e98f2801d1'),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification-review/frozen/CalibratedPanels.lean',
  'a94e075aedbfd323066e2e3d9c448c4324cba0a66024134621bf21b3f853a2dd'),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification-review/frozen/Calibration.lean',
  '4d6ce88b6f9861a6e16474b9fdae3cd0065c35bf2ee6999a4174490dbb5658a7'),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification-review/frozen/HitTransform.lean',
  '6ef417e8c3a354484fd5516ed88f89007916b0b5b7afb7f39fc2a697b5b9faf2'),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-identification-review/frozen/Verification.lean',
  '6828c55050390d08827d08324d85638909ea9ba6ee0b6057eb50cdcab68da426'),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/frozen/BernoulliAssignments.lean',
  '5479c27ef9ba926baf67cc729ee1de8745d72763fbfe81013afe3aeb0291e468'),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/frozen/EndpointLaw.lean',
  '1955766441ae48efc8fed4244c15e3d1f0f6db1ac538d5301b355f23f69e11ca'),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/frozen/GenerativePanels.lean',
  '4bfe487a3035317b2952c0fbe0edd5f0671b50c26f642c4ed20d2ca92f52ae27'),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/frozen/HistogramGrouping.lean',
  '96d836539a45e6b5052de22c0cee2d4ebc5126d65a7c8849acc4863ae6ff7e6f'),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/frozen/Model.lean',
  '2f34079118372c9d11362046cd7453bcc58d3a2eb235fb13382aa1c5675bd7b7'),
 ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/formal-route-probability-review/frozen/Verification.lean',
  '9e584791d95a6f1d9b49f369ecfc62ee83d8bc5f7769d5b0fe9b32af53f91387'),
 ('research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate-review/ImportInventory.lean',
  '7df4c8333864b66adbd1fff67095518bcd55d88da505f6357222eaf390c3f90a'),
 ('research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate-review/kernel-isolated/FalseConnectorPremise.lean',
  'de05da6fd8fa5b76c7a4ed4d769d955c9031b18670a74df320db49f668e60305'),
 ('research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate-review/kernel-isolated/FalseCountBound.lean',
  '5273a642875beb31e8bd135af55eec550c3ba6c05f8daa3b4956fe8fb27b69c3'),
 ('research/t20-live-20261009/checkpoints/CP09/t20-next-frontier-20261008/retained-interior-certificate-review/kernel-isolated/RetainedInterior.lean',
  '626edb56f345be531bade962af7f452d5d33f89b940cd63f708512742ac20e19'),
 ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/frontier-kernel-replay/CertificateFrontier.lean',
  '7120d15aa2056ecbc0609f88b3a15c057f1eedbf84125e8cfbf36880fafd163e'),
 ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/frontier-kernel-replay/Controls.lean',
  'e10019dad63f1c8b96dbf5a40e09383b1f5b5db1f165ab49f47aacb25a8c135d'),
 ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/frontier-kernel-replay/mutations/CostBlind.lean',
  '999e1df5851bef57266ccda86db59bb8c3437a3cf103bd01e02d9be01da2ceac'),
 ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/frontier-kernel-replay/mutations/CurrentCost.lean',
  '8a6264b005544897ae3add937d8fc25d9e6e3b7435d980921a374abf49050543'),
 ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/frontier-kernel-replay/mutations/InfinitePrice.lean',
  'fc028cd81562a8968c196a01a0b21f819e28b14a66fbcf5503efe54d041719ec'),
 ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/independent-review/ScopeChecks.lean',
  'f843892ea1afea1ce881679a3d068cd3421742c3755d27feedd54dfa92114ff4'))
FORMAL_PUBLIC_MEMBERS_SHA256 = 'e9e5ace0005db8af0d82ae41e2314d266300b05f50672bb4f1d2b507a97dc9f5'
CONTINUATION_FORMAL_RETARGETS = (('experiments/orthemology-v5-continuations/source-store/f3e08557b57a745bae547dc827755616cd6c6824bf1360441a72789036e1cd96.lean',
  'experiments/orthemology-v5-successors/source-store/f3e08557b57a745bae547dc827755616cd6c6824bf1360441a72789036e1cd96/AuditSupport.lean',
  'experiments/orthemology-v5/source/lean/AuditSupport.lean',
  '4ba3d9db5e9157c7c183a1045d82e3c40be887f9',
  'f3e08557b57a745bae547dc827755616cd6c6824bf1360441a72789036e1cd96',
  1024),)
CONTINUATION_FORMAL_RETARGETS_SHA256 = '6a433a1284ca0d1410afa33e9d90736448209077aa03bde028b3ee0c81896205'
FORMAL_CONTINUATION_SOURCE_MEMBERS = (('src-866c6ff6e74a67f2-32f3457897f7365f',
  'experiments/orthemology-v5-continuations/source-store/0f8e551de28b6bdf549e0d2ecba0932bb2758b8ff57aaf5f1cf5956d7d88d8cd.lean',
  '2e7c4caca6ce91ab6fae306e95e90ab32b372a708b0749a1634976cbdcfa9634'),
 ('src-866c6ff6e74a67f2-35cd3b8045bab054',
  'experiments/orthemology-v5-continuations/source-store/0f8e551de28b6bdf549e0d2ecba0932bb2758b8ff57aaf5f1cf5956d7d88d8cd.lean',
  '7f7f493c1c28d7250cc485ef49b0e04934fded40c79c54c4a141a02ac01eccd6'),
 ('src-866c6ff6e74a67f2-3e93323a3f29bb5a',
  'experiments/orthemology-v5-continuations/source-store/12dfbed26b887067f2bbd2a75930d038558b3a5c715100d7c25d3cfee79a7fdb.lean',
  '574d3f804893c9159e2c0c7bdce959403d787e8629b728cbcc553ad0150f01fa'),
 ('src-866c6ff6e74a67f2-65795fa696b7195b',
  'experiments/orthemology-v5-continuations/source-store/d3494436356f8aec5510b004e2a977c9946533f6190219f30eee2de511b53f4e.lean',
  '96434881b71ddede1a128613a0a2ae78dc7ec251c86e7cb272f6acd8b4d1f1cc'),
 ('src-866c6ff6e74a67f2-745256f635eb1b4a',
  'experiments/orthemology-v5-continuations/source-store/766ae9391263f193c6e84e16042281fb5e70fe680f083f0359b4b3c10f215779.lean',
  'a558442e5cb0735c38e1413b7ee2fe7969b288adb8a1767f3a6ad5c0c28a8131'),
 ('src-866c6ff6e74a67f2-8093c78798d6cca2',
  'experiments/orthemology-v5-continuations/source-store/8485a2156b943ce569af6f219d69d7d24b00b41b04b8225a68d7480d2d70522d.lean',
  'a227837d99e1e264eb108145a00bbc2de62a9e250a32e4409dd9d9d288c585e1'),
 ('src-866c6ff6e74a67f2-a6ebca3a4d81869b',
  'experiments/orthemology-v5-continuations/source-store/8485a2156b943ce569af6f219d69d7d24b00b41b04b8225a68d7480d2d70522d.lean',
  '2be6798c15d6c520422d5dc2f6514a201f9eb3ee664c7490a8d5da8068c8c291'),
 ('src-866c6ff6e74a67f2-afaf5bb6a3463145',
  'experiments/orthemology-v5-continuations/source-store/4c1d8a9d8a9a6ebec9f5e1a1ee41008b75fbfffeabbbd9ee489ea21982425a08.lean',
  '3652b78174689c1604fccaa37566a3836da8f1b5b3852eca0dd5ee0f8e3f8fac'),
 ('src-866c6ff6e74a67f2-cff78a4285d78182',
  'experiments/orthemology-v5-continuations/source-store/12dfbed26b887067f2bbd2a75930d038558b3a5c715100d7c25d3cfee79a7fdb.lean',
  'b3a05ed1d44137c6abec0a3fcf22b06f7f5f1a99e5a596792bd7628ebadb2550'),
 ('src-866c6ff6e74a67f2-d0674b738864eae6',
  'experiments/orthemology-v5-continuations/source-store/766ae9391263f193c6e84e16042281fb5e70fe680f083f0359b4b3c10f215779.lean',
  '242e74e9fa4b89562ec623a1b7a4ae23b40e7ec6cf64877fef0f37205cd44274'),
 ('src-866c6ff6e74a67f2-def38b90ccbec6a6',
  'experiments/orthemology-v5-continuations/source-store/4c1d8a9d8a9a6ebec9f5e1a1ee41008b75fbfffeabbbd9ee489ea21982425a08.lean',
  '2b5aacaddc28bf3e4faa4d42fd1ce77d126a5ce5c5de7a52fcd65f493806871b'),
 ('src-866c6ff6e74a67f2-f8db73bee7f4cf95',
  'experiments/orthemology-v5-continuations/source-store/d3494436356f8aec5510b004e2a977c9946533f6190219f30eee2de511b53f4e.lean',
  'f02d623b8dc81e65698f18cfdfdc6542636b10e9b2a56f72ad7a603434b43f76'))
FORMAL_CONTINUATION_SOURCE_MEMBERS_SHA256 = '2de02c958585f0089ab5974db3d8f2a6b3f443e95d9186b060f30b252778a447'
FORMAL_SUCCESSOR_SOURCE_MEMBERS = (('T16-SRC-9defcecf448b7eff64a3',
  'experiments/orthemology-v5-successors/source-store/b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183/PhaseStabilization.lean',
  '0fa4e6ae04a207cdd5bbb2f705ea1b657737f91853053b712c20e378e72b3f1d'),
 ('T18-SRC-e17dde5c235ce8f7cdf3',
  'experiments/orthemology-v5-successors/source-store/b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183/PhaseStabilization.lean',
  'b24f87865b69eab991c333dbf0444408fc7c9e10c5ab279880e18068e78e3c71'),
 ('T20-SRC-2b486650b115df568986',
  'experiments/orthemology-v5-successors/source-store/0e0636bf2cbd583b0a7193d9cc5985bdca6c5e52a0c895f01e9cd71b5677e34c/ReviewerReadback.lean',
  'd78131b36fa4ab0670ba27b5662238f9b698377353eafb4c69b59c2eb8d52b2c'),
 ('identity-src-238c1dfb4fcf213c07ba',
  'experiments/orthemology-v5-successors/source-store/f3e08557b57a745bae547dc827755616cd6c6824bf1360441a72789036e1cd96/AuditSupport.lean',
  '8c1c4338910e8e1ac529495a4807e2e72d3e1e6fddc9f81f2c8afd5d7c1897f9'),
 ('identity-src-46bc8a425b4dceebe493',
  'experiments/orthemology-v5-successors/source-store/f3e08557b57a745bae547dc827755616cd6c6824bf1360441a72789036e1cd96/AuditSupport.lean',
  '245581c6a57c60c6ad46a9c887f4b4329aa0f3b805539297eeecc4d9a1a6c575'),
 ('identity-src-a7b7307578252e460f78',
  'experiments/orthemology-v5-successors/source-store/f3e08557b57a745bae547dc827755616cd6c6824bf1360441a72789036e1cd96/AuditSupport.lean',
  'dc7b6b0f21aa5a16208da13244a9c125479d7d50cc19cc3c4e1efc35487b51ee'),
 ('s0715-179a29b309f46405321b',
  'experiments/orthemology-v5-successors/source-store/b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183/PhaseStabilization.lean',
  '3b9784a6f233553d033649b1fb0c9a7a566d974ca494eb3a0382560ff30b2847'),
 ('s0715-89259ffa9f43a905f9ad',
  'experiments/orthemology-v5-successors/source-store/b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183/PhaseStabilization.lean',
  'c52024e59ed9792eebaf2b859860595d1dfcbc4ebaa02e355f28dcc199f039a4'),
 ('s0715-c045f612cd9cf2974e56',
  'experiments/orthemology-v5-successors/source-store/b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183/PhaseStabilization.lean',
  '003f50b907bfbfd4bb689d26734e54b96ac7a14fbbca9e9c0c5e73c7d3f353fe'))
FORMAL_SUCCESSOR_SOURCE_MEMBERS_SHA256 = '5a1d6512928ca3a41b7c13608b3aa180de857f61b8bc7f1962494c936164fd9b'
FORMAL_SUCCESSOR_ALLOWLIST_MEMBERS = (('experiments/orthemology-v5-successors/source-store/0e0636bf2cbd583b0a7193d9cc5985bdca6c5e52a0c895f01e9cd71b5677e34c/ReviewerReadback.lean',
  'ca0db331d3eb2caf9747ebc15b2c387b7c858121b63923623e1968dc30ef4867'),
 ('experiments/orthemology-v5-successors/source-store/b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183/PhaseStabilization.lean',
  '5f8116b123ac3795d0f0054e6e13655a7846043979998a670d75efcef8b203b9'),
 ('experiments/orthemology-v5-successors/source-store/f3e08557b57a745bae547dc827755616cd6c6824bf1360441a72789036e1cd96/AuditSupport.lean',
  '03ff3847817dca83bcd36419819c2f4dc0ccb874de79e555a9c062d61da6c395'))
FORMAL_SUCCESSOR_ALLOWLIST_MEMBERS_SHA256 = 'a1b31d3d3d7e44f5f0c618851a4fd5cfa07bfdf2b86967c9b40774c41226cef6'

FORMAL_COPY_PATHS = frozenset(row[0] for row in FORMAL_COPY_MEMBERS)
FORMAL_CONTINUATION_PATHS = frozenset(row[1] for row in FORMAL_CONTINUATION_SOURCE_MEMBERS)
FORMAL_SUCCESSOR_PATHS = frozenset(row[1] for row in FORMAL_SUCCESSOR_SOURCE_MEMBERS)
CONTINUATION_FORMAL_RETARGET_PATHS = frozenset(row[0] for row in CONTINUATION_FORMAL_RETARGETS)
CONTINUATION_FORMAL_CURRENT_PATHS = {
    'formal/type-theory/' + pathlib.PurePosixPath(row[2]).name: row[0]
    for row in CONTINUATION_FORMAL_RETARGETS}


# Existing frozen replay contracts and recorded execution evidence. The native
# original tree owns identities; this finite selector does not create another
# scientific registry or turn historical receipts into current execution.
ADMIN_RECORD_BASE = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
ADMIN_RECORD_TREE_SHA256 = '7e65473d07162893f11ee6b2a1cc4cd33e4add3f20281d8ee4cbfecab68b5f0e'
ADMIN_RECORD_NAMES = {
    'docs/provenance/v5-research-continuations/checks/': (
        '00b240cf2bfd-scc-region-integration.json',
        '0a74eb642cc6-integer-budget-v3.json',
        '0d018cbe2cff-generated-history-slice-tail.json',
        '15e2b6abb662-prior-nonconvexity-v2.json',
        '24afae53f1c4-raw-concentration.json',
        '26d6d6369d07-sparse-process.json',
        '3dae38ab50de-prior-width.json',
        '4bd668ffbcfa-actual-cobuchi-cost.json',
        '4cde2d91223b-finite-law-rotor-progress.json',
        '549ba6a7f094-connected-author.json',
        '549ba6a7f094-connected-review.json',
        '549ba6a7f094-zero-error-disclosure.json',
        '5b59e4a2a1c4-conditional-as-preservation.json',
        '628d98dc2727-conditional-continuation.json',
        '748545d4cf83-tail-moments.json',
        '74b86eeeda46-runtime-v5.json',
        '769dc45d15ba-global-parity-controller.json',
        '7871eae3c71a-loss-obstruction.json',
        '7cbe94fa76f6-actual-finite-model-common-exponential-range.json',
        '83f1a917b40a-knowledge-author.json',
        '866c6ff6e74a-atomic-membership.json',
        '866c6ff6e74a-codec-pi3.json',
        '866c6ff6e74a-finite-frontier.json',
        '866c6ff6e74a-mealy-stage2.json',
        '866c6ff6e74a-mealy-stage3.json',
        '866c6ff6e74a-measure-frontier.json',
        '866c6ff6e74a-membership-computability.json',
        '866c6ff6e74a-operational-machine.json',
        '866c6ff6e74a-p01-canonical-projection.json',
        '866c6ff6e74a-p01-dependent.json',
        '866c6ff6e74a-p01-repaired.json',
        '866c6ff6e74a-p01-successor.json',
        '866c6ff6e74a-p02-pr-compiler.json',
        '866c6ff6e74a-p02-qualified.json',
        '866c6ff6e74a-p03-graph.json',
        '866c6ff6e74a-p03-native.json',
        '866c6ff6e74a-tagged-prefix-primrec.json',
        '866c6ff6e74a-tagged-row.json',
        '866c6ff6e74a-uniform-computability.json',
        '8d2cc96380ed-explicit-winning-record.json',
        'a45cc7cb3021-scc-global-parity-iff.json',
        'a5ea2c511948-borel-endpoint.json',
        'abce3ba5d09e-sparse-concrete.json',
        'b5be7775f6d0-runtime-v8.json',
        'c95f5175af02-sparse-transport.json',
        'd6f6fa5be514-common-observation.json',
        'd6f6fa5be514-compact-observation.json',
        'd6f6fa5be514-control-action.json',
        'd6f6fa5be514-core.json',
        'd6f6fa5be514-micro-static-equivalence.json',
        'd6f6fa5be514-policy-embedding.json',
        'd6f6fa5be514-recurrent-support.json',
        'd6f6fa5be514-seeded-necessity.json',
        'db6ccdc793a0-ae-licensing.json',
        'db6ccdc793a0-canonical-sufficiency-v2.json',
        'db6ccdc793a0-chain-budget.json',
        'db6ccdc793a0-continuum-repair.json',
        'db6ccdc793a0-coverage-boundary.json',
        'db6ccdc793a0-efficient-statistical-repair.json',
        'db6ccdc793a0-endpoint-law.json',
        'db6ccdc793a0-endpoint-safety-audit.json',
        'db6ccdc793a0-existence-aware-history.json',
        'db6ccdc793a0-explicit-scale-kernel-audit.json',
        'db6ccdc793a0-finite-audit-bridge.json',
        'db6ccdc793a0-geometry-delta-audit.json',
        'db6ccdc793a0-indexed-semantic.json',
        'db6ccdc793a0-mixed-rank-kernel-audit.json',
        'db6ccdc793a0-negative-clock.json',
        'db6ccdc793a0-negative-receipts.json',
        'db6ccdc793a0-orthability-core.json',
        'db6ccdc793a0-physical-budget.json',
        'db6ccdc793a0-polynomial-geometry-audit.json',
        'db6ccdc793a0-recursive-equivalence.json',
        'db6ccdc793a0-robust-repair.json',
        'db6ccdc793a0-semantic-core.json',
        'db6ccdc793a0-semantic-implementation.json',
        'db6ccdc793a0-statistical-repair.json',
        'ddbad6ca12d0-endpoint-atoms.json',
        'eff5fada59f4-upstream-author.json',
        'global-parity-control-summary.json',
    ),
    'experiments/orthemology-v5-continuations/native-suites/': (
        'sixth-cost-controls.json',
        'sixth-foundations-addenda.json',
        'sixth-foundations.json',
    ),
    'experiments/orthemology-v5-continuations/suites/': (
        '00b240cf2bfd-scc-region-integration.json',
        '016c63c30f1a-actual-target-policy.json',
        '0a74eb642cc6-integer-budget-v3.json',
        '0d018cbe2cff-generated-history-slice-tail.json',
        '0dbdc1f85fc9-global-parity-necessity.json',
        '15e2b6abb662-prior-nonconvexity-v2.json',
        '17797ddebb98-actual-cobuchi-cost.json',
        '1f321e9a7d97-scc-parity-pruning.json',
        '24afae53f1c4-raw-concentration.json',
        '26d6d6369d07-sparse-process.json',
        '332d0dbea81d-ae-licensing.json',
        '332d0dbea81d-canonical-sufficiency-v2.json',
        '332d0dbea81d-chain-budget.json',
        '332d0dbea81d-continuum-repair.json',
        '332d0dbea81d-coverage-boundary.json',
        '332d0dbea81d-efficient-statistical-repair.json',
        '332d0dbea81d-endpoint-law.json',
        '332d0dbea81d-endpoint-safety-audit.json',
        '332d0dbea81d-existence-aware-history.json',
        '332d0dbea81d-explicit-scale-kernel-audit.json',
        '332d0dbea81d-finite-audit-bridge.json',
        '332d0dbea81d-geometry-delta-audit.json',
        '332d0dbea81d-indexed-semantic.json',
        '332d0dbea81d-mixed-rank-kernel-audit.json',
        '332d0dbea81d-orthability-core.json',
        '332d0dbea81d-physical-budget.json',
        '332d0dbea81d-polynomial-geometry-audit.json',
        '332d0dbea81d-recursive-equivalence.json',
        '332d0dbea81d-robust-repair.json',
        '332d0dbea81d-semantic-core.json',
        '332d0dbea81d-semantic-implementation.json',
        '332d0dbea81d-statistical-repair.json',
        '3dae38ab50de-prior-width.json',
        '4bd668ffbcfa-actual-cobuchi-cost.json',
        '4cde2d91223b-finite-law-rotor-progress.json',
        '549ba6a7f094-connected-author.json',
        '549ba6a7f094-connected-review.json',
        '549ba6a7f094-zero-error-disclosure.json',
        '59af1e72d1f4-phase-stabilization.json',
        '5b59e4a2a1c4-conditional-as-preservation.json',
        '628d98dc2727-conditional-continuation.json',
        '748545d4cf83-tail-moments.json',
        '74b86eeeda46-runtime-v5.json',
        '769dc45d15ba-global-parity-controller.json',
        '781d33fdac12-global-parity-necessity.json',
        '7871eae3c71a-loss-obstruction.json',
        '7cbe94fa76f6-actual-finite-model-common-exponential-range.json',
        '810768c2edec-empirical-rows.json',
        '83f1a917b40a-knowledge-author.json',
        '866c6ff6e74a-atomic-membership.json',
        '866c6ff6e74a-codec-pi3.json',
        '866c6ff6e74a-finite-frontier.json',
        '866c6ff6e74a-mealy-stage2.json',
        '866c6ff6e74a-mealy-stage3.json',
        '866c6ff6e74a-measure-frontier.json',
        '866c6ff6e74a-membership-computability.json',
        '866c6ff6e74a-operational-machine.json',
        '866c6ff6e74a-p01-canonical-projection.json',
        '866c6ff6e74a-p01-dependent.json',
        '866c6ff6e74a-p01-repaired.json',
        '866c6ff6e74a-p01-successor.json',
        '866c6ff6e74a-p02-pr-compiler.json',
        '866c6ff6e74a-p02-qualified.json',
        '866c6ff6e74a-p03-graph.json',
        '866c6ff6e74a-p03-native.json',
        '866c6ff6e74a-tagged-prefix-primrec.json',
        '866c6ff6e74a-tagged-row.json',
        '866c6ff6e74a-uniform-computability.json',
        '8d2cc96380ed-explicit-winning-record.json',
        '90950961b666-actual-target-policy.json',
        '93fa38fffbbc-recovered-fourth-core.json',
        '93fa38fffbbc-recursive-equivalence.json',
        'a45cc7cb3021-scc-global-parity-iff.json',
        'a5ea2c511948-borel-endpoint.json',
        'abce3ba5d09e-sparse-concrete.json',
        'af86eb0bbb59-adaptive-parity-necessity.json',
        'b5be7775f6d0-runtime-v8.json',
        'c0c3081227ca-hidden-parity-pruning.json',
        'c3f900fa367b-residual-seed.json',
        'c95f5175af02-sparse-transport.json',
        'd6f6fa5be514-common-observation.json',
        'd6f6fa5be514-compact-observation.json',
        'd6f6fa5be514-control-action.json',
        'd6f6fa5be514-core.json',
        'd6f6fa5be514-micro-static-equivalence.json',
        'd6f6fa5be514-policy-embedding.json',
        'd6f6fa5be514-recurrent-support.json',
        'd6f6fa5be514-seeded-necessity.json',
        'd8de897ce9c1-empirical-rows.json',
        'db6ccdc793a0-ae-licensing.json',
        'db6ccdc793a0-canonical-sufficiency-v2.json',
        'db6ccdc793a0-chain-budget.json',
        'db6ccdc793a0-continuum-repair.json',
        'db6ccdc793a0-coverage-boundary.json',
        'db6ccdc793a0-efficient-statistical-repair.json',
        'db6ccdc793a0-endpoint-law.json',
        'db6ccdc793a0-endpoint-safety-audit.json',
        'db6ccdc793a0-existence-aware-history.json',
        'db6ccdc793a0-explicit-scale-kernel-audit.json',
        'db6ccdc793a0-finite-audit-bridge.json',
        'db6ccdc793a0-geometry-delta-audit.json',
        'db6ccdc793a0-indexed-semantic.json',
        'db6ccdc793a0-mixed-rank-kernel-audit.json',
        'db6ccdc793a0-negative-clock.json',
        'db6ccdc793a0-negative-receipts.json',
        'db6ccdc793a0-orthability-core.json',
        'db6ccdc793a0-physical-budget.json',
        'db6ccdc793a0-polynomial-geometry-audit.json',
        'db6ccdc793a0-recursive-equivalence.json',
        'db6ccdc793a0-robust-repair.json',
        'db6ccdc793a0-semantic-core.json',
        'db6ccdc793a0-semantic-implementation.json',
        'db6ccdc793a0-statistical-repair.json',
        'ddbad6ca12d0-endpoint-atoms.json',
        'eff5fada59f4-upstream-author.json',
        'facff25d4a24-phase-stabilization.json',
    ),
    'experiments/orthemology-v5-successors/suites/': (
        'D04-T07-ATTRIBUTION-ORIGINAL.json',
        'D04-T07-COMPOSITION-ORIGINAL.json',
        'D04-T07-COVERING-ORIGINAL.json',
        'D04-T07-CRITERION-ORIGINAL.json',
        'D04-T07-DYNAMIC-ORIGINAL.json',
        'D04-T07-HISTORY-ORIGINAL.json',
        'D05-T08-BATCH-ORIGINAL.json',
        'D05-T08-COMMON-ORIGINAL.json',
        'D05-T08-CONTROLLER-ORIGINAL.json',
        'D05-T08-SHARED-ORIGINAL.json',
        'D07-T09-CONTROLLER-ORIGINAL.json',
        'D07-T09-TRANSPORT-ORIGINAL.json',
        'T10-MODEL-CHECKER.json',
        'T10-NONUNIFORM-COMPLETION.json',
        'T10-UNIFORM-COMPLETION.json',
        'T15-EMPIRICAL-REANALYSIS.json',
        'd06-core-runtime.json',
        'd06-portable-cost.json',
        'd06-portable-runtime-literal.json',
        'd06-selector.json',
        'd08-g1-review.json',
        'd08-g1.json',
        'd08-p1-tail-audit-01.json',
        'd08-p1-tail-finish-01.json',
        'd08-p1-tail-finish-reference-01.json',
        'd08-p1.json',
        'd17-t14-occurrence-finite.json',
        'd17-t14-sense-finite.json',
        't11-dependent-all.json',
        't11-normalization.json',
        't11-nucleus.json',
        't11-substitution.json',
        't14-identity.json',
        't15-identity.json',
        't15-json-reference.json',
        't15-runtime-agreement.json',
        't15-univariate-reference.json',
    ),
}
ADMIN_RECORD_PATHS = frozenset(prefix + name for prefix, names in ADMIN_RECORD_NAMES.items() for name in names)


ADMIN_GUIDES = {
    'experiments/orthemology-v5-successors/groups/occurrence-language/README.md':
        ('e9a7bbd844b565ba3497650ed08f77bc8d960c40', 'dcf1e86bb630f7b4203d21587a638c94f2502c6e1a0b07fcf1f697c9e0953300', 11414, 2),
    'experiments/orthemology-v5-successors/groups/t07-technical/README.md':
        ('7cd6ff0393556359cecaee0c5b109a6cf8a05345', '3eb797cdf4925b80e21597fed04fbda0bee7a85f7bb5a141137fbba258cf25c2', 32584, 6),
    'experiments/orthemology-v5-successors/groups/t08-history/README.md':
        ('a49fbf2d3e0691495f5884e3a13ec475aafb1293', 'fb21186d2568c38564e0bf23f94df81d05fbad8fe39dcab23b6fd83b0291f7d1', 45079, 12),
    'experiments/orthemology-v5-successors/groups/t09-controller/README.md':
        ('f2b39f28134bfb2b8edf6406a90a51dcdaa1736a', 'de6b96e9afdffa7ace85c703990baaedf5b5ac7e70899d23b9ce3ad913d3fe6e', 17563, 4),
    'experiments/orthemology-v5-successors/groups/t11-types/README.md':
        ('06fd16b55848900bef9bb6ea1e1759c2b25b2cb4', '855990c6a98c740baa4bc050f5337e8a3b514dcea70fc3ea19a86558a9f067bc', 12902, 4),
    'experiments/orthemology-v5-successors/groups/t14-identity/README.md':
        ('09ea18f06905c0e5116375b2163737cf380755eb', 'bd58d620ac8a0dd0bbd8a3eb51e0c254b73cf14ae795a48dc19c347ee69b9961', 16523, 1),
    'experiments/orthemology-v5-successors/groups/t15-identity/README.md':
        ('eff9266c75ad72d7a60da622eb1e65ec5fe8a4e6', '03bdd90e71a1221722a27e39166f73b1ad0c14abd34c9a79773c6c01fc2d327a', 29130, 4),
    'experiments/orthemology-v5-successors/groups/t15-restricted-reference/README.md':
        ('fd3216e6d5c1a75c5f70260a3a66cc8194f69a92', 'a10ffec3e0baa17aa0307ba82f79cca7d85ea38edd212500bc8f1b21c171436d', 4451, 3),
}
ADMIN_PUBLIC_GUIDE_PATHS = frozenset(('experiments/orthemology-v5-successors/groups/t07-technical/README.md', 'experiments/orthemology-v5-successors/groups/t08-history/README.md'))

def administrative_guide_adaptation(path, original):
    """Replace only 36 original descriptor hyperlinks, keeping all wording exact."""
    if path not in ADMIN_GUIDES:
        raise ValueError('unqualified administrative guide')
    if path in TYPED_GUIDES:
        original = _typed_guide_adaptation(path, original)
    import posixpath
    changed = []
    def link(match):
        target = posixpath.normpath(posixpath.join(posixpath.dirname(path), match.group(1)))
        if target not in ADMIN_RECORD_PATHS:
            return match.group(0)
        changed.append(target)
        return '](' + 'https://github.com/theislampill/orthemology/blob/' + ADMIN_RECORD_BASE + '/' + target + (match.group(2) or '') + ')'
    adapted = re.sub(r'\]\(([^)#\s]+)(#[^)]*)?\)', link, original.decode('utf-8')).encode()
    if len(changed) != ADMIN_GUIDES[path][3]:
        raise ValueError('administrative guide link population differs')
    return adapted


def administrative_guide_source_bytes(root, path, allow_original=True):
    """Authenticate the original authored guide and its exact link-only edition."""
    if path not in ADMIN_GUIDES:
        raise ValueError('unqualified administrative guide')
    root = pathlib.Path(root)
    _administrative_catalog(root)
    blob, identity, size, _ = ADMIN_GUIDES[path]
    expected = ('100644 blob ' + blob + '\t' + path).encode() + b'\0'
    if _administrative_git(root, 'ls-tree', '-z', ADMIN_RECORD_BASE, '--', path) != expected:
        raise ValueError('administrative guide original coordinate differs')
    original = _administrative_git(root, 'cat-file', 'blob', blob)
    if (len(original) != size or digest(original) != identity
            or hashlib.sha1(b'blob ' + str(size).encode() + b'\0' + original).hexdigest() != blob):
        raise ValueError('administrative guide original identity differs')
    adapted = administrative_guide_adaptation(path, original)
    adapted_blob = hashlib.sha1(b'blob ' + str(len(adapted)).encode() + b'\0' + adapted).hexdigest()
    choices = {blob: original, adapted_blob: adapted}
    if path in TYPED_GUIDES:
        earlier = _typed_guide_adaptation(path, original)
        earlier_blob = hashlib.sha1(b'blob ' + str(len(earlier)).encode() + b'\0' + earlier).hexdigest()
        choices[earlier_blob] = earlier
    staged = _administrative_git(root, 'ls-files', '--stage', '-z', '--', path)
    accepted = {('100644 ' + oid + ' 0\t' + path).encode() + b'\0' for oid in choices}
    if staged not in accepted:
        raise ValueError('administrative guide staged edition differs')
    body = _regular_current_bytes(root, path)
    if body != adapted and not (allow_original and body in choices.values()):
        raise ValueError('administrative guide current wording or links differ')
    return original


def _administrative_git(root, *args):
    """Native local reads, with real repository/index and replacement refs disabled."""
    env = {name: value for name, value in os.environ.items() if not name.startswith('GIT_')}
    env.update(GIT_NO_REPLACE_OBJECTS='1', GIT_NO_LAZY_FETCH='1', GIT_ALLOW_PROTOCOL='',
               GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0', GIT_CONFIG_NOSYSTEM='1',
               GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
               GIT_CONFIG_COUNT='2', GIT_CONFIG_KEY_0='core.fsmonitor', GIT_CONFIG_VALUE_0='false',
               GIT_CONFIG_KEY_1='core.untrackedCache', GIT_CONFIG_VALUE_1='false')
    result = subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs', *args],
                            cwd=root, env=env, capture_output=True, check=False)
    if result.returncode:
        raise ValueError('frozen administrative Git input is unavailable')
    return result.stdout


def _administrative_catalog(root):
    root = pathlib.Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('frozen administrative records require an ordinary repository root')
    commit = _administrative_git(root, 'cat-file', 'commit', ADMIN_RECORD_BASE)
    if hashlib.sha1(b'commit ' + str(len(commit)).encode() + b'\0' + commit).hexdigest() != ADMIN_RECORD_BASE:
        raise ValueError('frozen administrative revision differs')
    raw = _administrative_git(root, 'ls-tree', '-rz', '--full-tree', ADMIN_RECORD_BASE,
                              '--', *sorted(ADMIN_RECORD_NAMES))
    if len(ADMIN_RECORD_PATHS) != 236 or digest(raw) != ADMIN_RECORD_TREE_SHA256:
        raise ValueError('frozen administrative native population differs')
    bindings = {}
    for entry in raw.split(b'\0'):
        if not entry:
            continue
        metadata, name = entry.split(b'\t', 1)
        mode, kind, blob = metadata.decode('ascii').split()
        path = name.decode('utf-8')
        if (mode != '100644' or kind != 'blob' or path not in ADMIN_RECORD_PATHS
                or path in bindings or not re.fullmatch(r'[0-9a-f]{40}', blob)):
            raise ValueError('frozen administrative coordinate differs')
        bindings[path] = blob
    if set(bindings) != ADMIN_RECORD_PATHS:
        raise ValueError('frozen administrative class is incomplete')
    return bindings


def _administrative_bound_bytes(root, path, blob):
    root = pathlib.Path(root)
    indexed = _administrative_git(root, 'ls-files', '--stage', '-z', '--', path)
    expected = ('100644 ' + blob + ' 0\t' + path).encode() + b'\0'
    if indexed not in (b'', expected):
        raise ValueError('frozen administrative staged identity differs')
    original = _administrative_git(root, 'cat-file', 'blob', blob)
    if hashlib.sha1(b'blob ' + str(len(original)).encode() + b'\0' + original).hexdigest() != blob:
        raise ValueError('frozen administrative Git body differs')
    target = root
    for part in path.split('/'):
        target = target / part
        if target.is_symlink():
            raise ValueError('frozen administrative path contains a symlink')
    if os.path.lexists(target):
        flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | getattr(os, 'O_NOATIME', 0)
        with os.fdopen(os.open(target, flags), 'rb') as stream:
            before = os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode) or before.st_mode & 0o111:
                raise ValueError('frozen administrative current file type or mode differs')
            body = stream.read(len(original) + 1)
            after = os.fstat(stream.fileno())
            current = target.lstat()
        state = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        if state(before) != state(after) or state(before) != state(current) or body != original:
            raise ValueError('frozen administrative present bytes differ')
    return original


def administrative_record_bytes(root, path, identity=None, size=None):
    """Read one exact original contract/receipt; no replay or status promotion."""
    if not isinstance(path, str) or path not in ADMIN_RECORD_PATHS:
        raise ValueError('unqualified frozen administrative path')
    body = _administrative_bound_bytes(root, path, _administrative_catalog(root)[path])
    if ((identity is not None and digest(body) != identity)
            or (size is not None and len(body) != size)):
        raise ValueError('frozen administrative requested identity differs')
    return body


def administrative_record_absences(root):
    """Qualify actual absences through the complete fixed native population."""
    result = set()
    for path, blob in _administrative_catalog(root).items():
        _administrative_bound_bytes(root, path, blob)
        if not os.path.lexists(pathlib.Path(root) / path):
            result.add(path)
    if any(path.startswith('experiments/orthemology-v5-successors/suites/') for path in result):
        for guide in ADMIN_GUIDES:
            administrative_guide_source_bytes(root, guide, allow_original=False)
    return result


# Exact original source/evidence records. Historical viewing never changes a
# status, source credit, control, adoption value, namespace or current result.
BINDING_RECORD_BASE = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
BINDING_RECORD_TREE = '9cd3f787299b774513f68837112d5f138b093dbd'
BINDING_RECORD_COUNT = 277
BINDING_RECORD_ORIGINAL_COUNT = 16103
BINDING_RECORD_CLASS_SHA256 = 'b457efc5f027c0179a573ef7f50e6f3f686e479d91ba4c6b676721623de2286e'
BINDING_RECORD_NAMES = frozenset(('MANIFEST.json', 'INPUT_BINDINGS.json', 'SOURCE_BINDINGS.json'))
BINDING_RECORD_ROOTS = ('research/', 'experiments/orthemology-v5-successors/')
BINDING_RECORD_CURRENT_REQUIRED = frozenset(('experiments/orthemology-v5-successors/source-store/138833be8349d7d7a1f5cc2790f9af1f920d52ed2e18d1103726f1e944ac9847/MANIFEST.json',
 'experiments/orthemology-v5-successors/source-store/16ee01f25a93117b0dd893bfb06b2f73a974594ef794650aada7e1231266b6d3/SOURCE_BINDINGS.json',
 'experiments/orthemology-v5-successors/source-store/4afd877fe463ed00698dd1e38f3a99c4de30d01f552577695dbd9ddff54b885f/MANIFEST.json',
 'experiments/orthemology-v5-successors/source-store/5705935996f3ed949f77d1f7d727d3b7970bf28778248f2ef5b643e0328682a7/MANIFEST.json',
 'experiments/orthemology-v5-successors/source-store/ccf9167bbb612d800a14b528407c6952101f5d217767922f4f074068277ee5fc/MANIFEST.json',
 'experiments/orthemology-v5-successors/source-store/fd3f503d6f1dd9ce5b164300154c9b4cc4cd477ed026804ff754338452815bd6/SOURCE_BINDINGS.json',
 'research/t20-v6-20261012/sources/06f23df1709d43f9ce21249202a012ab276861ac86f5471a7e868c466822a06a/INPUT_BINDINGS.json',
 'research/t20-v6-20261012/sources/fffd1bf1398f437d310aed8d3a54d3f0b7069d7d2852d5754babc22cffc49f18/INPUT_BINDINGS.json'))
# Dispatch filter only: the native original catalog still owns every mode/blob.
BINDING_RECORD_PATH_HASHES = frozenset(('002c5b9228aa3e7499c57b79a8796d941a9884cf688c422215ec8595d3a0ec12',
 '005a65f96af35a4c4a83c509b21d70df2979b22e3dce395d3a3b336da694bb3d',
 '006adae9ad6024ed93f5e8a5d593434abece417fa409fab3634c90249c02fc8c',
 '00ca11cbbe19ea85ed239d3bb432f229630ba04f7797c3b39e4311b6030aa904',
 '0146361e79bdd1d2ece4b546efd95d08b8c3029794e1292ac025be4fd9bcf082',
 '016c7ac27851df04484b672a2823893ca0c9961947e260bad89c845fee011f5d',
 '01ac4994152dc44b81cff446a26cacf6f6bb710ca9173156cc34184261f77dd4',
 '023a77782950298381dfe46b2e30e5b3018ef1608c5901440fef254b8b6f1042',
 '02a110de713ead7bc0f1d97f1d4b5ae0ce01c41cfb07e0eadc2d25a1184074e9',
 '02f1ff573e308423283f447776e94f77b749bccb5196aa6e0aa4a1d5415dce4e',
 '049228bbfb5dfffc3b1f02bd143aa6fa624d2bbeb51bd73b47081defb6928697',
 '060a661edb69d78b5d5772a715734f349857ce9f1998ad6cc40f677ef26c9c79',
 '066b0e0c80afff9a7df97cacf02018a5f8b2f0a247cc65fadd3082968a311f42',
 '071b2b82a8265919cb4419116f5dbb6b81490516128554526a62bfbc29d8605f',
 '0812ccd480deb99d2deef9424fae8047fb4cd861f189391cf0b2d250e5e82b1d',
 '09c26a96c9f4cdced2daec8042ce5c24408f11be4fb5e5910860cc190645ced4',
 '0aa8b5a82c3aacf4c7d63a63872de7ebd647629f116e045f039b3d1300bb8628',
 '0c944c50818e4286f4ae6a727c6492a2605f94229c4470392bcfc7df85170640',
 '0cb100e3a24ae26942bb1cd27cbc35ce86ae0c9e0f9a95ae1a9bb7a4c815e4c0',
 '0dd66f9d1d8a2c835e599536f47a7b449096f0ce9faf5ff3ff2decf495926baf',
 '0e8028539c7dc823fb20caca51edb1344d506e0d2c400951a2f3125b650bc09d',
 '0e94760663041fcb825a4deb6ca9ca5f840431673a86a5d30b50b1836822d872',
 '0f069659c9732bc353c8ab071a99c3021cce9236ddcc11d3cc4a6b8df05e9137',
 '0f1d2cbc12fd8491dba0ea8505fc6a977c694c1d0ac092e9b49a8b9a51f06542',
 '0f3da223a009b4d900bcff4c46828fa4535f6faca448d30b88f8f4cbf5d1447f',
 '0f5d3b4d5ae85cf09d1b92448f6446fa9a95ebd9e3f953d401af309202cf823b',
 '10a87971195baf82461a158a6d56790bb7c2ad3bedeb32590487096097946a4f',
 '12acb5d47815e3fb47ffc2262ce8f2eac914ac4d9f947bd58e899add622c9660',
 '13b800180f10bafedc52a853eaeec63999f204f88d42b72fd5396abfa630a0fb',
 '15414b10e07ac8a18704245bdc6ee07bccda27450a3402009e4e1203ffcb5af4',
 '1545e238eb9e555037b775b65f927dddfb11c1077cd7669ea92698c972453a02',
 '15faeb349919e7af8f834b763c1d9d5a2ba8dd99f48e954ea715e7da8cdb4366',
 '191d9b2df5180d1979d08dff2b1a9c83174781536a9b73d9337b34e172eb3f0e',
 '1af2fe03cb73f60450353518cda021b0bfcbbf76150fa619037324b7284c497c',
 '1c6da2b28f4f01e58a4698a14fad80cb38fd99368818c75475ef6c92300b6392',
 '1e8ecfa37b4c57559395221588ad2b8d61b8cd122ecd2b7455911d3b44f9052f',
 '202dba0e163e47f6f016fddbec7560f8f4f1d55cc23b94cc6f553fbab575223f',
 '23dad990a50f014667ab7728d2b45447c4e26f0c372fd1d32a0122fa41667140',
 '24926c8a745de476a82f4480a7bc9669f039ebb3b55abd432cc351211c1d13e7',
 '2521536af8164a80fc185d9f5cfb313f931626d109bc17e228cbe65daf79742b',
 '263070b259548a4540e1fb2357232b0df7b2913c529ad9289fa125fbd7a107ba',
 '2866701ce92bfbeace588eebf478e477e7e6d1baea68c8a864ae472c417d3f7a',
 '286c5f553ff9b74d4441b2daeb981811aa342ca04c9e8fa07f8a37647d0b80a8',
 '2942867e5318f23b54241d0df8623069a57b556749fd60a1f1dd7223f4b374c0',
 '2a1314a7da5bdaf4372c5cdea1c3f77c0ab9dd036d822c634ec4577087474b1a',
 '2adea39aca1543d04967ddfb38d6faacaf62036ac4e3cf6dd1718fd7630868fd',
 '2c94171b78fb00fd4119763430e98eb01b268c35c5d1b7cb14c89218e660ddc4',
 '2c9dd0389a9800db6752b7b143cc92f54a2c2fa9c6047a572232065d8c80a4e2',
 '2dcdafa6e2a64a9edd2b71f19fd72f61df36f7e18677b5a41d438f9a72faaa5a',
 '2e22e6bc0959ed37948f59aecaed31a88f66caa833175852ec3779b25cb7206a',
 '2e2c68d98bbe06fd013a1c72574f6f031e181d8442ae38b57007239388256dba',
 '2f8ed0a03b1f66f9d8fbd3e82ba6bc4e03250603050f144419e0c663b8ddb890',
 '2f9a826efe5c3365065f13fa59172926f8369ccc6341b2b6c9ee17d0bf7b8b9f',
 '2feb2f0702c4ed81cf7367e51a0a81b89df569f3f55926f88e6fd08f5615dfdc',
 '30e866a4011fed91a4735eb4260d78636447212f2d5b4a334eb47518cb3d2fbd',
 '31d1ef85620d63b19416882f387914bfc50169747b0d41ca16011594afabc6b8',
 '31d92aa361282f8c34557e4e00ccec493ab798d45606ac1355295db0f53a13be',
 '326187eb271bce0a3d12086dac772292ca5aeed63ce8ca5b47cd6fe2ee5fd3d7',
 '32fd2cb061b718356c5b46ddc893c7bfc4a5eb74479db78bdce1fb975b3d3178',
 '331fa89db01df335a7102894dbcc65492a4784a203c06d9590c5252d783325d8',
 '3350f38ed484b9b2219c6ac116d13cabfeb7ca748ad68741f4c8b73d2055454c',
 '351ac7f43e7a33f819a663dcbb00f8c48a48094e4fecd6a7219375d04fcde311',
 '37121b5471ffc986ad298cd6b89eee38e98d4fbee612e4d2745c159f59a097ba',
 '37155790bb7e0a32a787d4a4a5a69b1e322bfe4fb8a12298b5c711bd33391333',
 '37d54ce856b5241beb2c8fb6a53af439d9b627c3359af4ba33d07f51a6d28af4',
 '39794083b05e102c4185bbb5de8fa09b698d9b0e34219b51401ca0016f9b75da',
 '39df0455d48d128c5c6de6f6fded0198470277fd483bcdc3fbd857b5edab39a6',
 '3a04fcd75bdd2872702f402689434bb417bdf32ff36463e3c9097ceaf268c316',
 '3a3d9b03acf7a2a607d27dd2513fd305efcc0e720aa3651036dc2b1e582477dd',
 '3a66a7136fac7d91e583fcd2a3f009e72afe97b4dc8a8cabe8c810e6a43edbd5',
 '3adf1551b35c090a81e0e185f49250ef825c949c038ee0296722eb0c66998603',
 '3b8952dedd17058ef0d58ca3ebe1fa7ac3284d52597b1f880b3179fd78ab0b19',
 '3c2eacb618ec4999abcec85a9f51f3bf74d24638e37f2a1650c1be99bc0cc7f7',
 '3ce0fca365b638a037b7200da19390494cd08444cdaaa53d1e858736345022ad',
 '3d6591f0808014f1773a8ca37ea0f404d6f8f96780e4f55756ff9342874145ec',
 '3f12a98b58307e57a2e60c4a929d6c91083b49dc68a3adac63beb4615c0960d5',
 '3f5dcaab128023ccb0a17710f6f3cbfd0f98979426081be244ede68c7890c55a',
 '3fcb2ea190a2f63be6da27185dc4f505de5ae495d61cadf9faa9407edcdef4d8',
 '40950ac6b3d4c7669c87abe13904d59a03c52c360fdbc2187d1c7637a748ead9',
 '42c128e7ee52cb1dbdcb7bcd79301337a7bc1814b54d6da3a425122cf83762b2',
 '4364e1abb741a3e578ff8dc39cadfe1a1bbe131216e00af7d5c08f48db6465cb',
 '43ed422f0cd48e1e03b74698f471268eb98ddc6fe1349c7076026305a9361e5c',
 '468651dfe0e86a6a3e7e196065a848c8142c4e81bb64f1cf036dd6c4016fb629',
 '46bc6362a18647fb4fb6b9da8a4eec75bcf2f0780d878419f32bc6651dfd9987',
 '49c9f68856de4a22f2b7cf7147f2c50c4c71cf512670ca0db33879449beacf0d',
 '4b5dd3222d64d01d43468fedb73cf2d9014b57a5d06a18c49f3e791275d336b7',
 '4c6bef285698e7ef54ff11eba30d36804a1c78ff252f43a4f1b3f13147ca82be',
 '4cb54ff3c19c32d6c39eef349b2b1139829982207d268abf2bed35c7e7d90520',
 '4d6622610fad2f3018ec062f73c57441204427ccebad25b63817206d69aa879d',
 '4dc4359c623c3db7069da76b785fab509490293418a6ab139de00ef28f86a892',
 '4ddf8b9d78e2eb24f88c4302d83d6c70104515263a5232de7cbbfc50e490cd94',
 '4e617a9abdd83d544368adf772410abd06eb64b54b595fe709b457b515472f31',
 '50b96b616e36699e93a0d84d52b5ae8a70328afd926144e3dcc236896227cd6a',
 '52c242aef46b5b1cab06dd368c7a73c1000cc763ad647da369c7c186e3755d17',
 '540939e869185038d8ad54611a1c748960b7b3bf81e61e635ce3b569bfea459a',
 '5585c6d60dfa2ed861277b1571c747a4b87239ec8a2baec2e436e77834d9e1c0',
 '560785d90097fcbb829aeaab1f8352f35052076d3a957930b878e6f92a981c15',
 '57baea2579f1fa98340ca8c05c1d1f484be2b07fa7401ea5b8a8dcd856b03a56',
 '5990988da3647d59251a86a630fd03ee5e6fdf986db929c67d08429ef7222aaf',
 '59fcda6cf03dd489aa047b07402e8c8802abd6ff97f31971c4298f3441326529',
 '5cd66a12de638696feb7e09a4df7b5db819af86c197367f6d2192dde7765308a',
 '5d2b681f45c7a88b3df36baaa943bfb742ca6d5ec03b34f57e3445b2f91cc81a',
 '5d9ddbc686aab5a6e18105d5e17eda067f7ecb1d277379807a77e5f252f7d230',
 '5dbda47d09aab7f35d5802918540217bcae9cdbf5c77745e05c0a58a2800a1a9',
 '5e133d7fce2c4f2d0be5b55d66d9f06ec0d92c21acb84d7554ca47591a4841fc',
 '5eccf15d277cab100dc02d92ffe4baa8df47db3e07a59852f7f8ae71a35676a5',
 '5f225c544671bc28b7f89f8f8c0a6d02d1aad2e7676b62dc05af2304fc0b24e9',
 '5f22a8b8765bb3a0c7410b9e9b46ac609c95bac6a8e7dab1c6d3c0adf858ee27',
 '6063e7cfe3127804511b276e383572ec87155663d46283416d633188a4c79346',
 '606530071fbd6a5c67f96eb4dec5fbcbdca073e13ba72206d1bbcb0b882b8baa',
 '6138f58c80ea7708aaf5e0d62bd46a9994e78323bd69eb045e8f8f86555d8d7b',
 '6150a7b3f3298f18ac59e47f0bdab6d26ae77d0442dbecd1806f136684f10364',
 '615817d2b734134a2c0039af194d07daf1499d2234994d36a7cea0dae3925a51',
 '6182e4aa3be5d9dfbb0ee9298ed254c4646340967b00d98dd7bf465ca2847c54',
 '62f5490f1231a7e932fdc6e596f842584c7c49af8944cfbf505b6b166cf9fa70',
 '63e319814666805cb7ee476818a7baeb4f135bb67349275c3cf89f4268c08a97',
 '6477a4b00dec94a458eed10d3e43a7805c0624b00374e67219ab8920a4eecdb9',
 '64d71048e1bb675dca1f76fe48b10a52d62e4f315b7801d7fac90a64da1fe862',
 '65b4e1ed00760f92e87e0fcfbf55197d15d14dfcdd8c92a0ae414bfaf2e7e737',
 '66e289fdeae38a6aeba0fb9ab1d63a3da84f7582b8507c90e6d227c6e06e8266',
 '67be643c09e389f99b4d06cbc815ab8b156fa059975c0b1fb108201036520421',
 '67c12b9442f463c5aa525f2400655aff358ff76949446bb33ec1a3a68e30b114',
 '67d7f4b5f3b31e6e442399afb8a5cfcdafb37e6a396b73b87b9a32e426c482e8',
 '68e118b1ebf3bb9abfe24195dceccd908e34a870681f0fbbfaa8b6dbef74df66',
 '69b612667988050059f604cc580bb9ae05280371733af9e242dcc79575287d1f',
 '6af619463af57117151e58e92618ce56b9c1140995de76b81fd5e68499f05061',
 '6b6172214f00b206e9ce5818f74adaac1e42aaf6e6a3a4288d895eb86a9019d2',
 '6c5fffb4f409006b0388fcc08e09903b0cb939fe1f8ae6074c54806f257a2789',
 '6f750cddf03be71c26f192f679d98c4ae3e9ccece9e427c11f73d0700f0647a2',
 '703a5a78a7e453dda9a85a7d12184f3bc132fe86d72d948047dfb464dccc5b30',
 '71104e7e7c4477c8e22f69c09cecc2691c56e5f425f839ab0b91107e600c4b04',
 '72c112e837fa9b741ab5a183ddb6fb9ac3d79cc2852e2e61367e56b7fb057216',
 '73a386e332559f4abfdb426f5f5d2a45a97178fe9a170fd127241eb7f5d69d96',
 '73b69710c6d0f0ddc844556622436e7ad80ab3f302c15191d4f403b664ee6f87',
 '74324642f5b027f9ec0cfe42231e7ba7a96c18e815c333b007dce72a364f85d8',
 '7483370d36aa6e4c10967602c1688d3c6592c05406be873dcd867e349ac1d16c',
 '750fd16df02dbd7ad2075a8989ed37dcfc0a771d7881614f3309066d00d151a9',
 '776b1c97fc09be037cfc11278e95b361ec6665fc7087966ce1326ca9e93e4a43',
 '7be03002da6e94237cad8b9df5784e44d4c20557266aa9c8a6bfdcdd9dbdc33b',
 '7c2cabe2e9dc3fb222b81dd99b972d4a2f1965ad98025bcfd64172337a7ef18d',
 '7cd97319eaf4a90977d6928f1ac0bd2cb141bf12403841fb4355b14ee47ad295',
 '7e45c0d42550964abda2979706899b405d38026103477b740bc22dbaaf24ab40',
 '7f9d1a98d0d2dce8ba013ad6e5cdb211e099883f246a8084e2b8fec337c6269a',
 '7fd9944c874e496a248bf72f0cc73956c185b6b15e6d7ec14df756ae69a63891',
 '7fe0d9ccbf2b04168a7fb6fe8e3a6ebb65e10b41a0ab214a259a4bcc72aeea35',
 '7ffe3a02dfb8b51b9ec9384004bb32d8f198af1bbaa485888dab2cca5879e41e',
 '800b96132ad584859eda6b4f4f5882f26f594d26f39fa3fcf33df7960f959443',
 '827ff2b3c4805a2cd318b7fb86f5bd9547c5205b4bf697a0077760df94c92bd1',
 '840c138144a6d248f053f49107c9077c22a98e53e0bcff5f8a8b71fa4b8c4a0e',
 '863dfd0e5381183688c99057c3bfaadc4d7911a43064ad53e8e80ed8040834c8',
 '868142a87f63fb85ad89251e8583898d5a1cd082a48bcb88df9715a728599b01',
 '86e2f9bf82a5c48d76a564999d92ae054bf2d1e79c45c99bdde5a0ff9d55acc7',
 '872e211f22feabd3818b3bd4009f0ecdcd5133964b1baf230ab63230b15ec604',
 '87cedc90c90f0afc3ff4d8981befbd85a94c3403ba603579d981559d9e77fefc',
 '87e12e4f8f66fbae3056ed9e7122febfc331a6f7c52683468dd96f9f90b81725',
 '894a52721cc64e8f848f81dc351bd4ddaad33da4d8890f085c0d583e10ded466',
 '89739648720e881affb2251290c0cd80191f6dd6fa7849ede0575a20cc41adf3',
 '89c102ddc3639ba73b8241fdcbaca18b4b2e878f0fa2c8e000a00edfbcba88c1',
 '8a9c2e60272c1f11603081fcdafdfac57d0335d483a93aed5dfa36eafeb683c4',
 '8b37e8cbf16673462393f275a00a9523ec2d6a4adc60ca5361d10abaee671da5',
 '8b842708c58b00827b4067bedb296756fdd00ad6420ce5b13979be3fcf8708e9',
 '8bda8373b897ab62b8b951b02c87bdaaee655fa3392a6590b7204fa681358043',
 '8d498db8f731aecd606a898f8e7e972b74d0ce8ca907ff5dc8fd4c1959c02d35',
 '8f4fcf4148b88f5e7a06dc3a6f5ac8bac342e5ea75fa1b7a9e2bf58bc596b03d',
 '908e3fc6513ed50771ec38fbf4738b16565a95eac2e40565069a14655741fc15',
 '91f953b83de4f919779bb7eddad10deb679c3e1e16ecdf70d2ed6e30f3a92862',
 '9267b437aba98b03778df1f2012f682d35b602b63ed7fca3d829831cdbd27dd2',
 '932b096f36d7073e124a6b316a3e7615a68052d3d8ca0866d534f39a504f37b5',
 '93b41df4a87094b4b5e49c500c01ffb438f0260d145f7e271a9c279c1ef6bd61',
 '9477103a559afef359fd8c5584a892fabfe04a070bb613a681054aaab15c0365',
 '95b28749c13a093d46ab24a2aae0825fcc68dde4f55781f3bdc4f3948cea6e36',
 '96efca7e88f5c62801294aef258c1c49411363d694afe2278ac9260d50495e4f',
 '9960e6f9ea6f1ceed55372378223892f296c505e2d147cdde52f1898815d3af3',
 '9a75b6dc6acbf2cffc066bec7499df36669ecc4eafae98fc033437d85379a792',
 '9bf89b5d289e2a640908f5af745adb85a1f06809a8e2c7782d2e6ca16ce6d227',
 '9c07018446238dd62c6814b86da314e30ce56d390ea0bdff03fe659b5f2d2f99',
 '9c46308e47221f9921d72459b019e3d26af298ff573964b6a3364d3acfb464e2',
 '9de2e57fab5b14ce4cbc105af8af72f4721d53472d54278d1c3795cf6923cfeb',
 '9e5561a78dea43d193d169fcfdf0d1b824c67bd2e7cebd7c3eef46e5cfca1ee1',
 'a13b5972c4c7cb6f78aa9ed0637fd387733d5c5f63d50643d47288a7a8fa242b',
 'a33020bc0b51b0bf4725f87f9106dce58f9eca4e6185f62b4c4f19446f1f8ab5',
 'a463a847c340b68235d59862244824e89af7469bf0e37028b599ef9039181bce',
 'a58f0d3b955ffc5b23a6ec09d52928647356f199c8d73c8611aaaa6a08f1f984',
 'a6f5f72a86bfdc2c601550e9307ea20ff474dd9909e90c6bc553a4ef9c856ee2',
 'a76eec588682934ddde687033a3f9b7c64dc4a499fc6b39d61e1a7fd92bb6ae1',
 'a783656e50714eb3f7026329958e13b74e08f8980fff29192ad8e41c0aa74cff',
 'a8dc0710125f9582bae63126c8410cb4fd47b34d1037ae6e62aff90d65182bc7',
 'aa457cb1c9a8eb5aed9887f668780b8c0b925ffafa92ad19ec0770a86bc19ddf',
 'aa73bc461b0286829f41b8c67d6fa7217425b949dbfc4e3be547731a48defb4b',
 'aab8e0350856c0a7b1c9f3fea2a88d8e02304acfb0ab362297592d38fdced046',
 'ab28192810196657fc5e2a7b5892b211593f900da8d2ebbe425f0ed0af4873d9',
 'abe02c4889ab34dc920743347009eda516398d8947a00af9059c41c0ad761bba',
 'ac65e75191fe711f3f23152bebffb6721b88e3908bd0eb2e66c332b9b11f4557',
 'ac9d169625950fe0cb6f7a9c0c9383be30ec240b3a7924b45ade505062fac717',
 'acd3da1a0effcacc8e267939d0edffde45209f60275cbe134e64810d223024ca',
 'ae1732a1dbbd8f8b86ac7c0065efe2732c8e36d66003f5c0ffa49cb97f8185d5',
 'aeb9db5aef7db70be37a6e8978f395eaf97cc24a1dbbd66b1cc4b4c231548a5b',
 'b08ca204115ebe9f81b0c28a32db41e647d9eb49cbdef268a13b68ef25d819fa',
 'b095292bffe537dc11aaa30f26ad0d14501316a23986f9d757e5e83f69410dcd',
 'b0c265b2ddc58eccb88e96d7a3cdb21aac9230c60992e397fe5d43ab742ace31',
 'b0c44ea2a049b051f2fa4d0264b94666cc85895f65d2a69c033ca8a641cf6ab5',
 'b2d293ce3190c69f12c17985361ccdda48dd6ff2914a7e08ded29e19a1798fc9',
 'b4238bee1d6355196a6ea8e32d2ce0ba0517e25b09d1133de2f701c76bb142ef',
 'b526a840847a2e53c4687d035d8535216a4aa04ca470aaa1df1a4321f3b8b7c6',
 'b575f335eb779b8fa4ecfb80f7e4ebddad1710df83ab103dcb8148f30b33cea3',
 'b86036261725cd589a9eddfa1beb53a4d8c415fa1d63619bebd687f7ddfd217a',
 'b8e653b18bfd59ea2ed18cd3d40d0b4ff851a5b8639c0311161b245dd9d8c3b3',
 'baae3c9506273584a7f11274514de02677c8f21e1e5e628ffa1bc854aa353a60',
 'bacf67ece0e357f59b0913fd3397bbb68bf3c7db9ddea44147f0456ee8b996c0',
 'bd320044029505045b5483d6b44b580086a8491e1769445aca213181d5bb5957',
 'bd670598453d830460b46e9ceef4c889378fc45787ed60572ecf014e93f63ce9',
 'bdfd9c2df8178808d9914ee5aca99e5dfdfa86c8abb2e1773e14e173801823d0',
 'be81d796394f9794da306cd180accb03306414946d56463c0501572062aba29a',
 'bedbd5692157e02e9db1442c0ef63255112363f65b7cdb42a6cb3061d14b747e',
 'bf4e470869c830e338d83c371b779c3e079afdcb85ad7eec9e25cbaf27745299',
 'c04039e4c23a48cc45a8838bad66dbda2e4d49792d59b8546bbab21e5e1767dc',
 'c0707535fe2e6e0e30a5c1432a3506747a441d4bb67b049cf52c965c7a96fcdf',
 'c1e8c0ac222a97f9af47b56627422772d3b9e20d80f881378a7625c6efd45afa',
 'c24321153f01113a10b85bc1f958eea9da4e127303e62cc21f9f75dc582e2cbb',
 'c2d8591d1555ba3978e8205678a8dec40d5e0196ddd8749648902914f5a6e534',
 'c2f1dc88f543e553240dfd4584e96fbf96cace2f44661ccf5c5600dac0ba60b8',
 'c34bc5497a36a9d664134a4408a84a14f4213185c93b04204c830a10881d254c',
 'c48e9b7f84a4c7bd88d16e307a3bbe6ca140c390aee36309778ec433f71384aa',
 'c626de88def816a6376277ec3a8a1b29247e5293545f20a2e149a59217169314',
 'c664b53cc3ba97b666cba4ef39a9b776944959acbe089edf9d4fd2eafd55db06',
 'c6ab44565cd6b4aaad3217439c3e4909ee2e8a05cc34a0e884fa72a71d5cf32f',
 'c6d59a8babce65dfe6116b733774c43be22291fe35ae5a3de1980cd6bfbf0d21',
 'c71885d3bc0103b0902494235d908dfc4a1ae80b19a563a93c7a09b2da8f6c5e',
 'c7dc9d97ccd097fda7bed3df99ad0e8849491319b7e0112f5b7189a5a9ba4520',
 'c8042d607b7fd00b21c33ee59d6e53948ce1a4cbd8653a6e9568775555878ccc',
 'c8b813e48cfef6de3fee86ab762e1c4559d82518362a3a936a7077b2d843c7e8',
 'cab23bb15af56e8a74ec43e603286b78b96db101020df4a135b66a84f00f1309',
 'cafb73d867463626e1d01491546ba4cb310a4d41fae9d9d48ad46602e78c61c6',
 'cd818f27296d8f0ef3ec3fae28339a745b30db20cebfc9a5db90da9f27d18889',
 'cdf585c7b72d047ae429223edf9fe2a27151b79e7e5f47fb0ccba7cb684b4be5',
 'cec75f2ac58db0840333dbb02493a6a29d8e11e1308792494ab49b97f056fb97',
 'd0c27f33eae6c2c80f4795ab30fa57308e334f0b5e06126356759ed3019f8718',
 'd1489dbbc8bc35b5b80838931a44648d958fabae7964cf13a62da98e89d355f0',
 'd1bdb226584ee7b86536b1a7e3443b97324583929783762ceea1bc82d6b97e66',
 'd5eba985829bb7c62c9327cde930a64701fd59ece5f671a286c2eaad528bbd8f',
 'd693024698b15f7220cba904d2811a4e9a6d8c7dc98d4446563064408ea04227',
 'd75807c5030ed9572094fde6b5767879b8791f90479217814075632eb6d3a131',
 'd9133867e0504eaa98c698fed619286ce73c97f026b5109d212d2bfc8aafe970',
 'da0aa2e6d06fa7a85b2620b7db83da37b8e71618dbfc6743da0ceb5ea5813984',
 'da71d8bd418efdbc285092f2b3b3e4775c5a3c3344f9ad6ecf621d8e81242b4d',
 'dd16f40d9191335ea56c5a2414d04276981d56db7951eef090be91a1cd09f7c0',
 'de6b655c8cee885ea6d83171039b8ea898ab54e23c9f8a8973b12a49fdf137fa',
 'df0ce0c3a112b3719c3a34d0ef773eeb67174a856e338d963f3bf0de7a92656e',
 'e306dc273b9e9d3a921cfb2c64095778959f4bc618b113517c0b04c7644f001e',
 'e33f5c2b07d083d483f2ab44775412c09cdc2ef10e06ffc6f74a72ade63b4126',
 'e3dce5076a8d41d9a8df7b87f894059a35a9a5251057b1caded37b6fbf17c22b',
 'e3fdd5d58c9d4ff2c92ec11587a323704ea671d384d217a641a0ea40055e678c',
 'e5c44f5c0bb6b1b5feeee521bed3d4c7d0bf87bd0019bb67c506560546ec6851',
 'e83f05ae4980b834687e2f472bfc20beb686a7a657588d5437d2f362d65bdd94',
 'ea33d11b46247e5f436c59ac0e63dc830d8ca32eacaf9bc79390ba555e5e92fb',
 'ea4aafaa939b926cf4b8a5d9e2dafd8154f6fe22c8bc8f18a6cfc928f612e5f3',
 'ea70d2c912c8725990d9eb2afcd3a22291bc09c39390e2c325d909f9b9fa93ae',
 'ee5e65b904f6a2db7c446ecc1669912dd5dd4a379e4377b9804ef78d5d86187b',
 'ef323726b7210c860b4701ff6d0b74551c3ca80159328688ce80eeadb26f9f38',
 'ef9c215116031614c173afb45142e31e75f2e0783d6e86dc0d6240c325e5d945',
 'efbcd9e3b8d77c27cd9df659bbd8d53b3e9b4bdfd5785a6043e0a7b890132c73',
 'f053f29725151012b10b1e0098a2f6f0c391baf8fe4c164daaf4ff828d9ae18b',
 'f0e72732a6cb663288a00ae44acd02f8e79f365fa1770625d0c738d3dd9afd77',
 'f10b06065d0b93794652a36bbb3d470551aec41f681416033a1d7cc1c25ab945',
 'f351f17be5372e6d2ac952e36cc5666aa64028a2ac0d93a87832a96bd9c667b7',
 'f4ccfcaea9c94018dd7064c08302732ad0bca8c1356cfe3d28df9a4541b0c039',
 'f4d2e703956f6ebea7a1e0572c36cbe63ed24b4d37cefa7607cad7730661d911',
 'f7588280a8de74256f3a6662f438c35b97c6e5529096928c7836bdf798904c5e',
 'f7b4df4549a63251824424d4144c5b14100742459ba1137743ba569be117a076',
 'f7ee01855db9b9809847f12edf83365ac5b67bb85ef930a3c0ce52b21bb33314',
 'fa16f91c53286e3fe04c3c247d82440dd9c5502eb547b312165f3d3bca7e12e0',
 'fc6cacaf3ebc9144250c86860ae07cdfa789d0e8f4a54f57df75741838fb23a9',
 'fca662ef34706f24235e557a48cc09c0896c995e37c8a0adefbff4289b3a1680',
 'fda528fe3b81e780c9dea6773125be2e9afc7345b9ebe92254a0f40501320e3b',
 'fe3c8c93a810776d2d0426c093c88bd41dffe6f82cfdbaceb77a4a983b36d369',
 'ff5bfa168f0270e71a7eddf2e958a58754f04de2cbb6e1862dd8ba4b2dd31c9c',
 'ffa6d8b10ac3c06813f9fd3b4e4e16e0a9fd9f067e6f44e0217acde9873a5f2c'))
BINDING_RECORD_ROLE_OWNERS = {'docs/provenance/v5-successors/EVIDENCE_BINDINGS.json': ('1c724cd0a8e70dd2634ff5e95174f87a76da1263',
                                                          '5da3fc5207ad200f6677f7b12306655c3a6d1388c533a343cb1e3d0718a89673',
                                                          20211043),
 'docs/provenance/v5-successors/RESULT_STATUS.json': ('de45612a3d7d68b78ed65dacf4dc8a9080b00f9b',
                                                      '3e5917699c40b50fbd22ee4120b365b70bc32123b27d6ff9dac8eee9b1c5192e',
                                                      855613),
 'docs/provenance/v5-successors/SOURCE_MAP.json': ('4d61a64f4e9022dc24e517f26923980aaf6fdcda',
                                                   'db90ad110ccc9c6a63454cf91ecec4605eed7fe243d18883d3cf501c58cb4883',
                                                   4978847),
 'experiments/orthemology-v5-successors/registry.json': ('b623182df73c1d821d7d132ae092c7e7edf7abd3',
                                                         'a053989dc9c6dce6de4ec4208f48be8b1b0a66c284600b3dd17992c46aca7af7',
                                                         247365),
 'research/t20-v6-20261012/CURRENT_SOURCE_GRAPH.json': ('f6f7691f7f73abe581d72d438e74c5cb724bb4d6',
                                                        'ce15fabe3966d210aadbbf51b0d1213c45d6f9397a3dfebbaa66257afc32b5ff',
                                                        239538)}
BINDING_RECORD_PUBLIC_ROWS = frozenset(('0051eb5bf5bef81bb853007c953d98ad5498798cd16bbcb071fe182dafb2dec7',
 '02fa85d28c332df837783772c7f44a962a76d6f6a25bba725c7f39b7f59ac5b2',
 '0402ac0e9f901a716c76a252bb11eada8f0dd2eb09d9e3f7efe34efee2aba56a',
 '04d468950d8590f769e91804d91ad03d3ea4291d71e416dc095febd255f08e51',
 '082565d0eda6bc44eb539f441dab8a4a538f2a4722d5117527e46d0af7c0033c',
 '0c7f94d0621270fd901aa4fc5da6f1a6d3b130da585c72db649466761d474d67',
 '0ed796fd315a75ad3d6f12d25060039c4858214e6ed12484ca5b560d97ccf001',
 '10fb2f1fab1322c53808f70aa2e60b478d4f0700eda0ef7e6f3bd2335a960e89',
 '1284863b1dd50c072cd49a4fe0a1b6f994002638d8a80f87acc99088b5a55dbf',
 '131b00b78392302d79c0c5267bdd5988c00b293872afd96308e661b23165b452',
 '1451789885602b0bd37355e4d3696d7a92abe56c59ffa4a729b3074465a3685a',
 '185d49c808db354d62305c823b91ffe943c129dbf268bf6806c4abd4db1ee7ce',
 '195691bc2ed85537f1f575d1b72d37f98ddbe4a012f8286ab5963197de29463b',
 '1af1962c29ea94c4bf90c4df102da36f9fcf8d71ee713249e4d4a266fe43cec7',
 '1da2bf0592616c36be1012593f280c1afe3c918d17d7be4719aa263f8cf709bf',
 '1ffc981af3200614c72765fb5f19d0b4a145841b8898e37fe821b3c22a2bf403',
 '224400d933fe7aae5f1d30eb4fb34ea75b1b26450077a48278456072ede88d1e',
 '22cc4994e6f68061480fa1a7717b0dd770c9c183d68e4c8f141ce9ed710ad623',
 '23364be369b45fab02eeb1b4e3c4177507e3565eae87ba881cd36936d455418b',
 '27152cf774b9c5de3c63714352560be035ce9b9fa5d64e51b0ed704480e80704',
 '2866aeb96010a3d650a99878b93820b32cefe9ca71688f5f02375d2302619b5b',
 '2bb3e198cd68141ef80bf6dc00f4639d21d48891d6e01b4eec406fc612c48118',
 '2c33f1295a6da066733e8aa1565defbb82f1d5484ff6a3f77409c05e07b2d0d6',
 '2d69075c171a6451da230251473fe141d637f59e632b3e0ef776cf2a94c79a96',
 '2daafd81828b1720fa5d6daf01e0b667d3cb202c29bd34304914621402279b6e',
 '2f1def60962c1cf174b9652dc66143341ba03b382a18c03c5d09fa8422692cdd',
 '2f23754a6c7f0ac0770541a8e6069004f30d0812bacd8c465c3be78f3f409608',
 '327e71a7ee9e050dcddd186ce906ec8808d11f77beaac1c6cf8ac19f6799b0d4',
 '3c58409bad44f8356bdb29a88cef7f2f5dd9fe93a087e778c49972fa7b8c8585',
 '3ce7cd90e13c695486284fbbf14f3955922882b4bcd3f0d7bfc6b40e309cb6b5',
 '43efb3d24076174d4c6e3206d76c112af83d1efd1aa5355ad0418aed7b5d02bc',
 '4432a342cf2f169500b2ae39c85aa9853be0162978b82093971e0f8635c6448f',
 '45cf5767883b230bbb7478b3402b04c38c3e0c6f7dbb8cdc2762733a9e1a048e',
 '4b0bf504be5f90b467ecfa617f12be0077d27a935301aead0fdb5dca4689fd71',
 '4b6d8c463a8e53d26a90ded0d236116301fe60a8889e547503ae28cdd259f6d3',
 '511239c3f4b40e9b76d70be0d7653b35f97fd431876ffde674a21ce234393e8f',
 '51826602b68b24ab9bd02d9396b92ae592ca0810ec511166f9aba5a69438a306',
 '563e18b61d75e59518e17121a6fdfd54b8aa3f9c7812fc12394d5f949a888daf',
 '5652898cdc527fb614c4942220a55439f77d7dfd947909acc7224d6aa89e13fb',
 '57704fd83563369f4baed59ecea5c6c754c936eb1d11dc62921b41ea8dc8277f',
 '5c13d84ec81f0b3662b65c9596c2455cae20cf5ba045ecdb9cd797b9140797b1',
 '5cfe5e4d2898bfabdaea5804953e0dccc146362d5783b1dfe09ce1a4ec07b265',
 '5f95be5f6beffb0706ee3a56f002af11e3151e162ba8d5f2713511d9e9f3b622',
 '671001276b0303751b912ed4313533a406788b05c0d564c773417a3225ddf4eb',
 '671b9afc30bc35e76e6c8d00422f659ee0daa5a01b2919b01587c4d3477b593a',
 '6f170d9b5d2a2ce134ef82b3f06293a0f6b9b29c3310a86814f28e4544a2d708',
 '6ff11247980d4817494f37b1aa8efaafa194e7d0fdb78c1fd128ec752ce110c0',
 '7131631d50e3c6560dad0602731cca7cdf1413685b89cb211e57b06288d50a57',
 '7311e1d0c597062b44d66269c515ff51fa558dc7b3c836eff36441cfb29071fe',
 '745fe8087b724a05d99b98012e065180ce7e7e6e465d6138a746c66f1ef4eb13',
 '78f953cb5dfe1ef14bbebca77e4773a40d39513a8de4e485e8ee6742e2e2a729',
 '7cb040de08641df8142a8e096309754aaf8f91be1e9488266f434da8cc281c8f',
 '7fcd5d93e47eb533f77bbd5bc47762507b9344e5de29f0508449c5944bdfe79c',
 '84a84b3308676bd7003f7942bb564d83f73e6ec3d248374920dd6f988ed16cf9',
 '879fa84bc5157d1fb3049becd430b247ceb7824d635e6de09066041e07046d65',
 '921199477ea6aaeaefb206c9f03da50f1de253c1357259fac963f987fedd7a6b',
 '9914bd9d90fc5866b21a86105d85a72d51e74ee8503f4576ee189f923e3275b7',
 '9d2d1191fe02b87d011e065801da2ef8ace98b6814e29450c25ef803e5abddff',
 '9d5a2fc799fd8e458da609fd8430831213ad0ea7bcd79c36e83c774493b38a5d',
 '9f376aa3be38363d3b47a8d0d4143fc26dd9bdd6e1b3c374569e7e8840b63d14',
 'a2ce248880c56a503504b2a8775d38f86e0ba29c9dce8f81be077504f9de18fd',
 'a85c02a895d8ddd0133ce0aca6e82b7c7ebf4b7c41c7ca0de74274efaf74af71',
 'acac9c29b02f56ab14ad22caf4eef87c63f6878c1a867aceeb6e0a59039bb9c9',
 'af52b38ce6209be85bc2aa5238e8d5787f0d9f0e48c85915481f069ecf47b3a9',
 'b2b897b7deab80c58e7418ed0a8a996346e8c3505135984ae3f3fdfcc69828b5',
 'babd0a986eef6911168874100e46cfb9ca6f55ae729711d91ac0cedb8b4d0760',
 'bf5ccd6a4cd62608f9862429f13f14b0f9d7005fa635a6d062c2cb4251b2eb1e',
 'c30eac4fe781117e0ba5af8b533005e95a974974d7b02bc81c1f4d177f6c479a',
 'c41bdac94195ab2e3e2f967de81bc93fbfa62b9de1b5b267812093f7d6b1d743',
 'ca3a22906b86655e31de368b0a71ae3b8902f50210645de8c30d43418e0e68d1',
 'ca5d2699f67b82dab3d2892e08560d957e636c352cb4ec0670641a92a2ac79f4',
 'd464289a01dfa778adf3c6cff719d0b70270c2381c57697b19f06f07aa41ee70',
 'd55e7dee27b3d58d82d336c7e68ee2d58f01c14e3c7c0baded2e08a8535a1336',
 'd6fb8155ff49bcff48de13015b75c212d33ce347cbd587a15b225f66e18e2199',
 'da6310035158d77918181b055df12874329447bee1e2fe9dd9d15391344a83d1',
 'da83c66ce42bd4b30c4c5ca498514d0007259b93b5d49e0b6b66d526f6e1ad42',
 'db4fdedbe69540da77db1c5fa63b66b220c883b89f5bc8b2cea36e9b2b51ff27',
 'dc6ca42457144ca13f289b86b817661c9cd125a62c473159840aaae6cc161549',
 'dc87005db591c70734c1519d7cde31c9d72028a8016346066e51ce594d1f42f8',
 'e194c94cbac13e33136db2f3fdfde7c2cda5b7667a0d34f7a5dd0414c8edae54',
 'e88edc5f31d704750dda26c505c50651fd89a1a140b41e221fc68a5e8b9f399a',
 'e91d052c52a3d5f13f836adab69a48a902656cb2861e325e804444712f7d1939',
 'ea58a0c70794b6f34f56e0ec4be2150d6f266ec21d06ba04a0ed689ce2aa202a',
 'eab61669049321a45314616f837966ace07251fe8dd420c04813418dd2c66305',
 'f18e0ee417e0897c541a947b4b65636de64025620ae3cb549a9a4831240b2e30',
 'f61cfc61b11759d33e48113b738da03d54798110661a39090b7d259d11549e62',
 'fad1d3f36b16223fdc5a37d8580744e16cf2cbf42a2f658a1b15737a4588537e',
 'fe427688c6bfde96be340211ea4f60fa2599c2916059611a1573cc9e0d343f67'))
BINDING_RECORD_SUCCESSOR_ROWS = frozenset(('09a823e526cd5bef346941bdb5fc49791d9cf9a7b00b40c14064f6b78d85c331',
 '1c98e6e4120d798921f2912d38bdac131a2a09d59ffd2e61bbc726246934a43c',
 '38c4f0b79c5b09bfa9410e69aabe9978b2bb29a367e039f1a19cdd5c1da53c23',
 '4b566ece6feb60f48041a2524dc67c6ac2246660cab9cca3dba0e36776d5bf0d',
 '547c4852fad59ae292cf88a3e2ecc288142eaf440bff73380007184a9ce50a9b',
 '58e5e29e4c5a3b9dcdd2aaa9adc58dc8e94e5959dd0afc6ac9d43c3c47f098aa',
 '6c0d6cb7036fa2733755ec50160e68888357fa2e62abe3d79e0e9e0378a4b8a0',
 '77a77cae44eac41e80d77f68e02b08f0bebe4bf73d0958e9f5a67bfdf3e1599f',
 '7fa3e9ccec2a6d4c8874e3c75d49917459cbab28166ff6e82fa41265f2cc18d4',
 '80a814403aa8a088f8369c1d77a542da4b6a1510c6e3ac8ec7d0cc13ac196e39',
 '9f1e196692cdc1e42d8549d3c3d12f9835a7c2b16f0e99da2bfba0938318687f',
 'ce2187c4583477a55604a67a836f546961f2f29d1ecebb73ea735fb271ceb15e',
 'd0254ffea347cd76b37230f4202194034b5600ad8b29975a7d616258529f2a25',
 'd88697b9eaf33886d7d25daeb104a06ea57c097c2de1d04605de8c5ffc606358',
 'da702d40c77b54e50edeeadcb31423a41deac31c81c0818a1bb093fc99b2b201',
 'df1d759974c6840895f1c878a3475435be2a61af431aeff70c4396181f488770',
 'e4702e24d465d8e1642cb65725e8bb5d53443a14b55419a2268cf7ddcc39eebf',
 'ea355cf69c25763140a63679f9d0ac4fbce22acef0260a5217a6e35808ca3709',
 'f6d49938a2133fde56ff2ecd7045d00e600f7216b0fe595a6a23b6920d79365d'))

def binding_record_candidate(path):
    """Cheap shape test only; original native membership is still mandatory."""
    if not isinstance(path, str) or '\\' in path or '\0' in path:
        return False
    relative = pathlib.PurePosixPath(path)
    return (not relative.is_absolute() and '..' not in relative.parts
            and relative.as_posix() == path
            and path.startswith(BINDING_RECORD_ROOTS)
            and relative.name in BINDING_RECORD_NAMES)


def _binding_record_root(root):
    """Check the supplied ancestry without resolving away filesystem aliases."""
    root = pathlib.Path(root)
    absolute = root if root.is_absolute() else pathlib.Path.cwd() / root
    for component in reversed((absolute, *absolute.parents)):
        try:
            entry = component.lstat()
        except OSError as exc:
            raise ValueError('binding record repository ancestry is unavailable') from exc
        if not stat.S_ISDIR(entry.st_mode):
            raise ValueError('binding records require ordinary repository ancestors')
    return root


def _binding_record_catalog(root):
    """The original tree, not names or a new registry, owns the 277 identities."""
    root = _binding_record_root(root)
    commit = _administrative_git(root, 'cat-file', 'commit', BINDING_RECORD_BASE)
    if (hashlib.sha1(b'commit ' + str(len(commit)).encode() + b'\0' + commit).hexdigest()
            != BINDING_RECORD_BASE or not commit.startswith(('tree ' + BINDING_RECORD_TREE + '\n').encode())):
        raise ValueError('binding record original commit or tree differs')
    raw = _administrative_git(root, 'ls-tree', '-rz', '--full-tree', BINDING_RECORD_BASE)
    entries, counts = {}, collections.Counter()
    for item in raw.split(b'\0'):
        if not item:
            continue
        try:
            coordinate, name = item.split(b'\t', 1)
            mode, kind, blob = coordinate.decode('ascii').split()
            path = name.decode('utf-8')
        except (ValueError, UnicodeError) as exc:
            raise ValueError('binding record original metadata is malformed') from exc
        if path in entries or not re.fullmatch('[0-9a-f]{40}', blob):
            raise ValueError('binding record original coordinate is duplicated or invalid')
        entries[path] = (mode, kind, blob)
        counts[mode, blob] += 1
    selected = {path: entry for path, entry in entries.items()
                if binding_record_candidate(path) and counts[entry[0], entry[2]] == 1}
    vector = b''.join((' '.join(entry) + '\t' + path + '\0').encode()
                      for path, entry in sorted(selected.items()))
    if (len(entries) != BINDING_RECORD_ORIGINAL_COUNT or len(selected) != BINDING_RECORD_COUNT
            or digest(vector) != BINDING_RECORD_CLASS_SHA256
            or {digest(path.encode()) for path in selected} != BINDING_RECORD_PATH_HASHES
            or any(mode != '100644' or kind != 'blob' for mode, kind, _ in selected.values())):
        raise ValueError('binding record original finite class differs')
    return {path: entry[2] for path, entry in selected.items()}


def is_binding_record(root, path):
    return (binding_record_candidate(path) and digest(path.encode()) in BINDING_RECORD_PATH_HASHES
            and path in _binding_record_catalog(root))


def _binding_record_present(root, path):
    target = _binding_record_root(root)
    parts = path.split('/')
    for position, part in enumerate(parts):
        target = target / part
        try:
            entry = target.lstat()
        except FileNotFoundError:
            return False
        if stat.S_ISLNK(entry.st_mode):
            raise ValueError('binding record path contains a symlink')
        if position < len(parts) - 1 and not stat.S_ISDIR(entry.st_mode):
            raise ValueError('binding record ancestor is not a directory')
    return True


def _binding_record_current_state(root, path):
    """A current role owner cannot be supplied by the historical fallback."""
    if not _binding_record_present(root, path):
        raise ValueError('binding record current role owner is absent')
    try:
        entry = (pathlib.Path(root) / path).lstat()
    except OSError as exc:
        raise ValueError('binding record current role owner disappeared') from exc
    if not stat.S_ISREG(entry.st_mode) or entry.st_mode & 0o111:
        raise ValueError('binding record current role owner type or mode differs')
    return (entry.st_dev, entry.st_ino, entry.st_mode, entry.st_size,
            entry.st_mtime_ns, entry.st_ctime_ns)


def _binding_record_role_context(root):
    """An absence cannot hide new active inputs, results, receipts or sources."""
    for path, (blob, identity, size) in BINDING_RECORD_ROLE_OWNERS.items():
        expected = ('100644 ' + blob + ' 0\t' + path + '\0').encode()
        before = _administrative_git(root, 'ls-files', '--stage', '-z', '--', path)
        if before != expected:
            raise ValueError('binding record current role owner is absent or staged differently')
        present_before = _binding_record_current_state(root, path)
        body = _administrative_bound_bytes(root, path, blob)
        if ((len(body), digest(body)) != (size, identity)
                or _administrative_git(root, 'ls-files', '--stage', '-z', '--', path) != before
                or _binding_record_current_state(root, path) != present_before):
            raise ValueError('binding record current role owner changed')


def _binding_record_bound_bytes(root, path, blob, present):
    if _binding_record_present(root, path) != present:
        raise ValueError('binding record presence changed before its read')
    if path in BINDING_RECORD_CURRENT_REQUIRED and not present:
        raise ValueError('active proof, result or replay binding record must remain present')
    expected = ('100644 ' + blob + ' 0\t' + path + '\0').encode()
    before = _administrative_git(root, 'ls-files', '--stage', '-z', '--', path)
    if before not in (b'', expected):
        raise ValueError('binding record staged identity differs')
    if path in BINDING_RECORD_CURRENT_REQUIRED and before != expected:
        raise ValueError('active proof, result or replay binding record must remain indexed')
    body = _administrative_bound_bytes(root, path, blob)
    if _administrative_git(root, 'ls-files', '--stage', '-z', '--', path) != before:
        raise ValueError('binding record index changed during its read')
    if _binding_record_present(root, path) != present:
        raise ValueError('binding record presence changed during its read')
    return body


def binding_record_bytes(root, path, identity=None, size=None):
    """Return the complete original record without replay or status promotion."""
    if not binding_record_candidate(path) or digest(path.encode()) not in BINDING_RECORD_PATH_HASHES:
        raise ValueError('unqualified original binding record path')
    catalog = _binding_record_catalog(root)
    if path not in catalog:
        raise ValueError('unqualified original binding record coordinate')
    present = _binding_record_present(root, path)
    if not present:
        _binding_record_role_context(root)
    body = _binding_record_bound_bytes(root, path, catalog[path], present)
    if ((identity is not None and digest(body) != identity)
            or (size is not None and len(body) != size)):
        raise ValueError('binding record requested identity differs')
    return body


def binding_record_absences(root):
    """Actual historical absences only; direct active obligations cannot vanish."""
    catalog = _binding_record_catalog(root)
    absent = {path for path in catalog if not _binding_record_present(root, path)}
    if absent:
        _binding_record_role_context(root)
    for path, blob in catalog.items():
        _binding_record_bound_bytes(root, path, blob, path not in absent)
    if {path for path in catalog if not _binding_record_present(root, path)} != absent:
        raise ValueError('binding record actual absence set changed during qualification')
    return absent


def _binding_record_row_digest(row):
    return digest(json.dumps(row, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode())


def binding_record_public_bytes(root, row):
    """Bind every original public-row value, including source and projection roles."""
    if _binding_record_row_digest(row) not in BINDING_RECORD_PUBLIC_ROWS:
        raise ValueError('binding record complete public source row differs')
    return binding_record_bytes(root, row['repository_path'], row['public_sha256'], row['public_bytes'])


def binding_record_successor_bytes(root, row):
    """Keep original/private and public identities, source IDs and credits distinct."""
    if _binding_record_row_digest(row) not in BINDING_RECORD_SUCCESSOR_ROWS:
        raise ValueError('binding record complete successor source row differs')
    return binding_record_bytes(root, row['public_path'], row['public_sha256'], row['public_bytes'])


# Exact historical status sources after semantic-owner incorporation.
# Existing277 and duplicate aliases keep their prior routes and guards.
STATUS_RECORD_INDEX = 'research/t20-live-20261009/INDEX.json'
STATUS_RECORD_OWNERS = {'research/t20-live-20261009/INDEX.json': ('08341bfd44725c42af1048aec08fcad5b51aadfd',
                                           '9cf4bca6f4162f3a0426dba75949cb13482544ba35876d6e3a4dc1d2e699241f',
                                           5956771),
 'research/t20-live-20261009/README.md': ('3a93bf5c75cbbd0796e3edef91a7571da4eb2771',
                                          '1bea43d34528443aedec67f7a58a92d04b173e87c4d068f018499f9c4651d49d',
                                          107789)}
STATUS_RECORD_BASE = 'f97b01417de9d95a44cae4d3a3ac71d1e29f984b'
STATUS_RECORD_TREE = 'c8ec5b28d65fccc5a2f38c6564384fcd682089e3'
STATUS_RECORD_SOURCE_COUNT = 749
STATUS_RECORD_ALIAS_COUNT = 811
STATUS_RECORD_CLASS_SHA256 = 'd2f1a3b21bd01b67a94e7116d3646c6eed048538b92a63e01bb36690f9b23b29'
STATUS_RECORD_PATH_HASHES = frozenset(('0050201bfa3ea89e862a4fd5161a23ce6cde31a8f015373000bfe8f28badcb56',
 '0070357d1620b9683322cf0078c9fca43fcf156b5227fe45d00b2c253afabdf9',
 '0189c4df98224d8e75b8cc49ffb70b16f750572a67e64719f1746b269cc28dbe',
 '0267f30e4130f32b8cf6e2773ad33318e1863c7ecfac06bc89fcf5c5bc6ff246',
 '0308379d78e3d225fc049c0137b7e751de95dbea577761dd318c35748bbc641e',
 '0435304467e4a69c6207051bd5ea1f56c70e9faf36cac65212b23597681f5878',
 '048596caf3d220271cf02ebdeff54ecb811df1419f06be7865ebc97fca28b5e2',
 '04a5d02b266475b4fc43dd324d2a58fa2026523f3ba66faba09eb3164962a42a',
 '04bd93c448385d944e25a36fe248ab61779ab4d737881492b4dbe3a2bba6d881',
 '05477ccaaab0782a7a589add6c8a0af2ff4b585e9b84cca62f8e49328202b222',
 '05798e3a9e56130a1e6990a99679cc9bc5aa1227557bd431cb013ad82f315ddc',
 '0593307ce55b38ced153ef66bd173089eb7a0b86ed4d9d37425ee7894123a85a',
 '05d34db45f5a0b37f8bf726afc0490bcb40c231fc7d7f6e45fe93f97bf12670d',
 '063d158f6eb9b39f092277b83ef9dd4bae4169011ef64e63d57d1dafd1166f1b',
 '06545578104b84d2aa9cea77b08ca2322d6f99fd83aa7c60918e963ec6cb56d3',
 '075bcad472c1f0ce7cfc8616939d2775cfb0ce894216f2f79cd753e311bc3d4c',
 '07c1209a3cd4dcf58f99965fca9ce5480fd735eb06ed3cffa030605002dda5f7',
 '07d1c9cea7a89550471445bf59d554123e4f8ae92105c0b08b7160b7350f17b2',
 '07fae636b724a020e829c78563bd45f32b4a11427486ca45733b8b0db8cee5f5',
 '082f3ef77a3fa1c6414e7be26f90c58f277fe7ad5eca0a68dafd6da6097bc24f',
 '08697a5c912278dcfebc00078e7c2cf750fcc6976e2d821a1368ddead5aff0d9',
 '08bb73409065f06b02e97e51fe59ba8013e8dbdaed2d0dcd39ace5ab2ead6dbb',
 '08d8a245da82240c0b0342272118e1ee1c820199052189c751dd86fe74e75d95',
 '08d9c7ccd7cc18aedf126b637782b6edf650ce353e9bff026b49d95d5ac18ccc',
 '09f8823999bafc67459142c2f2744691423d939027e1850a96b77bb0ae9d5cc5',
 '0a6250feb32aa162c249ff95804954f497baaf3b59233caa087c2a44a8f808e7',
 '0b2bb4cd93ad028463d5f7c74b8d24beafea436a87a9aa76fe537564c49364c4',
 '0bbb43451d3f1dcaaa28144705bdc79d9b57eebd46b0979d6fcd7a027a621ab7',
 '0c3ee14364dd4abfa08fa4fc1e6863aa69894bda7aae869d54269eec19c49094',
 '0c537d5300ef28e020d55993cb960c086c9803f35cbd93e305b6eb3b3a731d97',
 '0d25ecd4fb814d2cd3234668f164bf8d83df7aa28b269f15973a4278e1072ec8',
 '0d4067211714c4b4afdf11195dfdcc7ebd51b9a7d7daba5b50044dd3cbd7bd2e',
 '0d434f22191daac5b4874504c44efb1021c06cf482b088f7e4da121a1ca8c3ea',
 '0e78e55b20c50e87d06387f101edd741828e57379c72b669ffe6f4d9fe47babd',
 '0e94abbaa507051b2e63d682ef4f72f8ad6ee1cb1f59662c9ebdf91140f141a6',
 '0f26ac8ab52eb026ec3b6cead94af2d2712bcda6d01843a68179d9b0f1cbd732',
 '0f3bd91056bac39e01a8a2586a5e35345228aec4ea35f377cfd35a8dc76f4954',
 '0f81f325677bb6b2394811d8295a9531bf7227d861ac56664d22613e17469240',
 '1092b8b2cc768275ac602107fb338bc1b1f1a46902fcd74559f6e5de2c29610d',
 '115d382dce2c83db46546939b9dbf01bdb0c22c116482c71d174fbaf2fc5b6b3',
 '1238ca645bff8d9691ee353a3a49af004e5c88621fdfea81da8af59415a7e20e',
 '12ac3020b0e59ae5bc9417cdfe111a3dc168ca61abe4626d3fa499f88f4c0712',
 '144f7e5d312c4bb812dae917dec33f0ace2d66bd80d7c8e8064181f5b3a6b7be',
 '147d4997a87155fb16a2196c64b2f2953aabc5be4cbe625e275b4efdce335c83',
 '1492af9e1ffe190600eef9b8d3f58ae201f14069698a07cb7f5e95c6acc6d9ae',
 '1588ce0c8712b849f12e45ed96ca468ed404bd1c782b9a0e4630eef4801b8323',
 '16ead1474c50005314f1eebf8e51dbd417ecf3d896a7aa313e6ca11dd68b551f',
 '17f72f3eb1748f95e81b2a3e3d9b2d8fbd18c4f78f503f68ac57fa52494d6b97',
 '180c6ba99521037d38d153cd704ebedeae6120a7a2962f1fcd11c148d7406e43',
 '1894f008698f1c6995dc520294797e6ff8b40069ac69d8402784e1345e5ac295',
 '19167034076d58b8503978aa2fde50be70884cb0e482b51cc470ed0dfd6e98ea',
 '193d0d994be94b05824c8407749f23e4449df9df4c5fb803f60dad2b848c115f',
 '19705bfd161285023c2950566c72b82178b49b82f49aaf51db2b85ae790d6f22',
 '19b726bb712d57c0f29a9ba0f7dbae8dc1b2a05623a9eb7e8abece58a1388367',
 '19da2ca5060fef958c5dcee9dc126be2946006931dd6f6732bf91db5ae53540e',
 '1b52fffc4a1f533763c82e58df9f77f3c5593781971116c7dfa8e399deebc151',
 '1b6c87aeaa533d35bf6d0076bbfdb8701ec88145afcbc1db4b488233c089f1ec',
 '1bc2052b6ab6bf40388fc0aed45b12b5b020b10c17a5342a489f63b2c4b917cd',
 '1ca88a62491deb1a8731dfc7ecefc03e2f098f4d158c32de78aded555b613c83',
 '1cb5162109e3573a5eec9a9436ca7161d2e7ddd2eb2092fc9787e1af74f5dc37',
 '1db82dac75285a81da12268318d0e9ab89dac07391701bb9ee6d24969e43edc2',
 '1dd56d6415da0f6a093efdcde26ac9a523d710cd30af92aa5d25446cf8ce606f',
 '1e15eca49cee19c94870ba47466dada06499cc27de5fd60db2c5b921c4cc252c',
 '1ecae3ee3bab88f04d60d56a7813c3b0e8b17ef6272a69bfce62df23824a3d98',
 '1ed8a2be4e3866e65893911e45deeb7a51f730ccee49e1ac869659b9d6c1914d',
 '1ee16401b672ea60992af1d0716a41f3450f6b79acfec6875a42cc904ef9fdb6',
 '1ee8a593f74e3bb200df02f4eb2c5efd1c9ed7479d1cbda42b223dbf5d19fe88',
 '1ef7d0e87c75ef9b79d7131fafa8a595f94d7e12b1a410fbdc3e0079b9e7ea79',
 '1f08bd64fae184d812a09f0bbf3395ddef502701cfcc4371f1ce7e9d5890cea8',
 '1f80f71c5236138d756f3bcf798530a612e795e8bff93d6b52819d2c1634c154',
 '1fb06e118accd795f93d3441bd29d2c5deb47313c8e8f303b39c6c1037132fb2',
 '1fd1966c5f2a50eeb94e9b9fc663b99176dd3662118874c665d84cc01f6c9d0b',
 '20c7d22e7d3fa1a431e014329cca6738bdaa43705cd327b7cde634d53bfcc759',
 '20e2d451b0b75d211f1d23946f3af19d7f8183d7af02760abe0a32c1e7d8bcf8',
 '2101ee4e4660f7e8602e0ba4e8054f9e879f1a262ea57c3e28bdd863ccc15f59',
 '219f871383ed3b157609c7584b1646a8509a25d495526c60191a98f740bf4431',
 '21abf16b99f97f5b1e80192c854453e51f269d9bdc8f457f76cecd1c481ba328',
 '21f45588f4c9d53a52c5ea63ed03328085d91d87f10fa9c98ee57a61362ad8fc',
 '21f5c502ecc404a49c43bc68d3f50a02af64415fca6992fc6636955c4bdc9edb',
 '22d86c4cc27da3d14d10ac953dc2ad9c0d114ef5e6c924f6641696d5dcabc78b',
 '2312b8cca14c1d280efc77d0e607320e542d86106f84ffcddf24b681c53c9a22',
 '237fc8fad85c770b25a920a0cd00859d6537c36d7232ec1cf66a4e505f6b4ead',
 '23d2a04d8c2633b634197bc7679bca5a6e6b7f4714a641e45fc5ebf04ac37241',
 '244f8d4f86495cbd3ae5ba2f5e2b631983995b8e94474bf01f1785cd3c9c1731',
 '253683c1c61ec2d9fefc4f09ee8683c1e69799bdaa17e6a1b7350dffa466d717',
 '25c13c65d3f56fd0b57616d0aa68b274890accc78be86020a401d419b6e13b69',
 '272f0eb73b2b061b440824f5c51fd336ee0c96aabe0e1d6b9f7b3a397de3bc44',
 '27809acad0b6ec81c35cd8ecb3cf3ea87e6a0c518d0cbd1e874140deacc4c3f5',
 '28831fef6cdfe9fff880d720a7b2ac9e7911d4d25028287fb5026b13ba0ee0a9',
 '291e8fb5d52f3e2a9f81303f419a2e6885350c07144668fc38fcb2b7f2a4da06',
 '2ad213803d8a0e18314dff28f257d3706d9900d3c0c8964fad1ccf3f7e6c60cc',
 '2afb60e374b79de6700580dcee99671ada529cde400a9546d804c00f0966e6a5',
 '2b5f0dbcb4f59eb5bada7609201a321940604cbbcdc36f4404a39d3eeb90cc3d',
 '2b7988955b2b6d0452dd722eea26c7e62a2c09d67856235696a35c91c93fb21a',
 '2b95110e066991961ffe96db672c380da63ef368ab1183d8ead6cc547ca9943a',
 '2c1af4b90d5823993912ec502f510f8334ce1418dd4af45bc940369a215ce01c',
 '2c50538ce43ca3a40ef54e890d12d49a4b6dccf57417b3204837121b8c541231',
 '2c713f08f3d2a533a4fb49b1e43bb0468aabe162b10c06182011b3bd5887558d',
 '2c85483f5b9511ab112d8b21967c66625c61b7179881b5f2886c3c50e533096b',
 '2cfb0dd67082335c7e029b9edc29d80e3fdcf6dde63ed81b724ef8fa6602a3d8',
 '2cfe2d3bea61b367a475b4a4f8b89063afecb87ec4d87cd81fb88f81e9b5f60c',
 '2d2a3c8f4087cc58c7bd23d2a53e13fefeba3cd394c2af187ef0622dec64c7a7',
 '2d3841181bad1695821644da0c7113cff42a547fce845830f144592e1f4fa165',
 '2e7baad437c3b8286485dc05c19dfb9d99cbb41022743eba386a1c4b2d402019',
 '3004f8f15c3a6141f567d4c244519bfc7a353ad3cb1c9133aa65cb0db9abf312',
 '301095e3dadd55f1f555d01de754ea8e0d75fb695f397427e0a7c5e9bc88b61c',
 '30af5c63979d409fc7403e27253b4646fb1eef3b52adf69b068ed5f72c3f0e89',
 '31a3e7bada2b660b8a7ec5dc0332bdd38459c8dd122bbea258754ce9fc5397c4',
 '31b9be091b654146410c93434f645f1cc4a10ad365bbb6a80ceb9891fb0b46e4',
 '31d0f05bdce7a2ad95a35995bda54d897d9f3e6ea6c517f6ccbb1d437e63b785',
 '31f7e3ae0b51926f01a6a82b0d249a2c107283c01779ca3249db404803d99fb0',
 '336f2e7c57805d34a545d39f0f37406ef3fb5b93a622324b4f8e44c05f8dc69e',
 '337004d115bf3c7a1c7a3ec1fbcc886a9e234250c8b2da71f3fc1d038109779f',
 '33b6d7945f93a28dcc846ef27ab1a0d2438d68b979f409e77550a2bbcde3a610',
 '33da9a31233245d6056236dc3e09c6e03cbc8b6a2423181728e9f9ab2fe9063e',
 '34f1ebdb4bb5b0b743d8067f1b1ead7c4a3c5f1b9dc74fdd2e4a4ae2f8fd36f5',
 '34f8589260863e4e564200b49d683e2a101c084169fdc5337597f55ed8b7e29e',
 '3530feace89a2bde9bf3ea4b42b531ccc50da2e114077315bce7372b1b30a5d5',
 '35ef339ca8fda8718713f97d049c7bcb4c2a0ca8217924958ee4b73f73b14b4c',
 '36efde6c75fd001fc5f0c5991124c6ddac2116af1a34157c205248afb73674c5',
 '380224a96b005fcd57fb492aceeb74bcdfdbd245300ddfa4ffb666ca7d398299',
 '3832ccc243f1ab84efa917dd6ab3eeb7b2b5caaa4134029e072b25c8ea332606',
 '399038552ee77710e43cf1d46f5e6900c679cd83c896e2ddc3ff01238faf826d',
 '3aa6b132242472c56961176d3f3c9d872b7573578c8554b5dabaef63813a52c1',
 '3abbf7cafeefda561c35c01185a5c1149d7224cab25af57beaa2dc7ec8a35f83',
 '3bbf497a6c15322ffca983ce65943e4eca0ad23a37649ac4e7a11d9536c76c15',
 '3bf5aee5d7f6e6a928f3cacef76b41d91be842aa070c1cb1fee54e0b71d05ab4',
 '3bf901d46aa212680e2ae446b544bafd324e82aa700ce6fb7c6c4579e328a5ca',
 '3c1dfdee1cfefed984c5fd86d7445833368d810f42c24a511f51b919e247358a',
 '3c346b3716e407d389560e337b68b23db642cbbc6ab3dfa89674eccfe5897b85',
 '3c64d0a82a2c659c4c28c33e54eacdb8cdb24a3757c2590b7dae821be833082e',
 '3c83cd5971b412089b0815408546bbc28dd90c243367f2cf7e57b353f04d6e50',
 '3ce5fccf2fdf744e6a93960d025b08609eb696dde6a980f2f00bb6f4549d10be',
 '3e34732717c355e01ab3ee6f006fc642a3ba9e2f239495279ce302c6c036bcb0',
 '3ef54edb9ad87067906f0b6eb7715ee6350883a584bb80d6e1052e3e438e5aac',
 '3f442a9d66eb81ac2f367fe7b2c35d386dda7022f810aea1d522a404d132651d',
 '4000b46804a0625b13773f5be7d7698971fcbfcccb8b243f1304d1412ea1035d',
 '4117555165d1bb5832a18b0ddaa2c836e89d241f2e0331461412c66d6f0228b6',
 '427e42c05ab8bc21edfd4396f10f9b3c54e5fba2e5c10fcb9ca1991540735478',
 '4366c16252ae4eb431e715a256b2a49d010f583281540fd26c41b2a91bf881ea',
 '43773cbca927c24803cd81079b2561239b2f3f7a93773f096fe2bef930d08496',
 '43d01074e1456b8466bccf5472d2b662dde342f2e55b69bcf3934bf877dad058',
 '441e756e1d2f5e4e40326f2811c1b7a0f42d9eb9e9e3edf51383ae038c5cc3a0',
 '44b45d146d0fcccc9013b4dac2f49774529e65249745808175d3f33655acbdf6',
 '4518cda613cec85e6e9b181cdf49cbbb9081ffd3cad97f5546614b98a8e8b3ea',
 '451f6468f22dece4f42e7fa77e8753127607b2905648ed6b37a12a93dc75a466',
 '4558773ed7960e467d37e0d8bf19da4fb0bddd83852035ed856ae80734226d8b',
 '457dcd3d9515a2b5cef6d16fc16b7024d52e763a6210faac95898c88d6e8c6dc',
 '47351017484c721f22f00c05c5a749e482ae14914677bae0be10259606703fc5',
 '47d174ac3cd4e705a80028b8375c879710125013e2bb7e7d33d42b111bec1211',
 '486fd52c941254ae0b2a529436df3649d00b698fa35c27491a1d3d18c1f50bfa',
 '4925dad92b494b24e8d526488ae2e67a352dab4bbd5691e4a7b17c0664f1b6a2',
 '4a253fa55376a3a5129533735652c5cbd930b0fc2698335b4289a254e08e1604',
 '4a8d5ea5ad267584a825ad2cf2ab2510164b97958a1c9bb5bf3d8121f7e5faad',
 '4aba12511323477a3f0fee6268d560ae1ebd8847efa55ae3b4b5d6aeeeb5adbb',
 '4ad77e0fb41f3fcc6b1ba79b526ddbe84c4ab4f49a03b3821344531e32f893d5',
 '4b5cb4c94df9e8c67a286e393f2662c9998ad5a104d40b861221a83909b6ef27',
 '4bdaddcb0fc337bc8cc766c50e6e8e367498567ee7749f421d15f02896c9edb8',
 '4c8db52854a5c33b983e2b15a639509371ac0d4ac19a9f7e2f4ea46cc4ef18ae',
 '4c9248c2669be62a66981757ff050c5a85f3dd557cf590d824f20feb2fcd1773',
 '4cea2335fd494e0f037c10a668dbbceac4d898c3251419b9f1b1ec2275af8c65',
 '4d311e9a59f8a6b11096c48f284fc89ec6abbd5a8e7e79298c31cc2c3e5eebbd',
 '4e23200081f0086c904eda9f4df43d8bc889adb58680fb813389e7f87c049f3c',
 '4e57ee2cf177004163d1feea0c2566df23b7a21907495f8368f1eb088c744ff4',
 '4e693d659600f142de829c501e073aba25395a7509d4cbbab857bb078eee33f7',
 '4eb2eb31933f285dca19d6c3a166d8a6a33ce9a788411d80e9eb9a5ac5abd390',
 '4f14861bf1e16dd3f82c6ec8cdfa73ad32dd44a0a85cf2a33fc93749f84a7ca3',
 '4f220e1d9c1b7e77e543e162ca8182a785a16e2211b3d34e5f10c20e189ab3b6',
 '4f47800fb08efb637c3a4d8c35507f7ee614590ad61038b28d759282ca6cc79a',
 '500c8f766c75f2a3dec78a208d5e3d1d9e9488e98472caa73bf73b906e35af54',
 '508024ed5023f1b46f3bb524e1eb45fc01374775da3282cca66ed279dd758e78',
 '509dbdd96b640ecdff5fad64851fab6b4ba35a70968cccd72a0b6449e89234f0',
 '50fc3ecb73ee163c98738f3d208a82047c14df4be2477dfd542d2145e9578cee',
 '516dbf45445cb0dea0b4cb006a75840e4dccdfa6fe6be0fc46d8319841b09310',
 '517b00b7c7ab2fff2e77b9bcc517674576238435e5645af955c190c7aeec95e2',
 '517bdc707bdf2b444306626cfe303c4a26351f6427056a0c7adf593bc2048e5f',
 '51a78895cb7c1f533a58a8584766b444a01dab29107b4116ce3d17a0b10557db',
 '523e3cffbd391e347b5e0171a4aae55a8a792f56238fc872d63c5cae06e4a8cb',
 '53ce1b306912e22b613193a3475c10e6d2aacf4a425e6e322cdf7e2ea7c06c34',
 '53fe73e91c0aff59f409e4bacf82255e456e7122662558c770f18401ef7c856d',
 '54ac89685ceb49df643ef8d13996ed621c59396af89d25124e63c38ab9c8eb37',
 '54b43be97ddcd0deba46da56f7f7d952fdbf1fc27f5fe282909839bf95e06214',
 '5541429b9534bcfc7884c2d25529fda7e85ec636c90f82f0f92bf86871cfc748',
 '5610b5a6b14502ed60b3732cc9ca321d68afd26ba14632c07e6ec1587f77ef7e',
 '56294cf81d120787397ece064a2c31b341a5e023882a43ffabba935742dd5d2d',
 '564a1604ccd054fe9d7b7833d5044f79f713f29c4a8cab7fa3405b4b8d92711c',
 '565ffa22058353c3575f1602a54b75bcd05f6b26941222c9a9ffdb8bb28086b2',
 '5719f0367024d15486a9c623519f7084a9a6e7b65bcec0e8134b151c2aea98c2',
 '574b9a97d6c90be42928f178ff45cc10da043d63f496e71c1b794841e7677d3f',
 '579da17b33dd4f85e51a24643503f5fe888f11ce342c39f658f696053ae2b0c9',
 '57a33ce6b45374d13d60c13b41e05c3ebfd3f52e7d2c8481cf81eaece4976512',
 '584852c2707cd752f4ea2dd32a5e8c574c3e6b19322d7da84f3d340bdf2fc258',
 '5887251a72cb4fb8ee6767daa80a7e853d55c9cf0aa37344b3eeba15ac379e28',
 '58fb824beba494e62026cb6a79f513721efed04b1072fd36abc60d56d3fb6f3a',
 '5968aa4310d208672ab46ebe9aa005d9904af374913d6ca4f5e91974fb519060',
 '59e28e8db06729ae9d98797555e21fe2b65e89d76ffcb868ea82fc35a3eea9ba',
 '5a7c30c6f78861150f09d3d8812f9f60bde3f7923233c622bc823bf0c2aaba94',
 '5a944c13c39d882fb14c136b4e75be53d975a23a4bd95f10eb157d4896f449f9',
 '5b05fc6211b86ccfe52a3d8f0be61b220b35b716d79c3c8248975152abe77b55',
 '5b286e74ce9ec94a3ce6a15a1e1c0239fc4ece7e48dd221d04bc31cc3725225a',
 '5b50344f0fbad872c9273386a79bec9846ea2b37ef8e2415df77aacf8d972a5b',
 '5c1843b94fd6762e34debf5cc6aae8e47c33cc6b2304445646822eb2ecdc5b0d',
 '5d5290b1535f95477844e00bf465e76486c683785ff7eca07194af12885bcf2e',
 '5d8699a9fc8a158883654d0ece15adc1a9ed06f794ae0a0d66c9459d4f55fb6c',
 '5f55a5dcb75ec0d35c174921f131f7a2b00147e0fc71d4d1fc34a557c3c46c3d',
 '5ffcc23a1eb486d7a0ca7776e64e4aa672f38c9e486a50b1a7666608e084e263',
 '6056f66a89148b3166749f785e50dfab2bd225063963ca112035c35b305309fb',
 '6058b19deea7632f426a8a37cde1c49f078589ae8a704f9863286874de09d165',
 '609672ea040d5f438360c5430185ca07ee404b6675d36efbde91df9fa6030a30',
 '6107487aa554a42ab0076cdafc7a1192f1705524cb56085783b47b7981f20d6f',
 '6173b96b26021e78e90fef00bbc1dbc3573154e253f8dcaa80b7762a521c72b5',
 '61a3ee341980fca94bd915a4cc4274657e0c8c643669018f56914941e2a2d49d',
 '61bb8b53b06f1468824b23393b64d1bfd74d85f8c7cbba6f427fc20de2a23c2a',
 '61d6aa25846d4c2f637b76dfb59e23ed3fe0b4359f5179d5eb144ea27b650537',
 '61de59729d0401c1ef13a83cf170a1dd65212aa155f0dbce9f91c0642939e58d',
 '621b1dca2a03cf744ee564d806e0b98970ca0f86984206ddf6e8be36013bb401',
 '6329dc6e1d333bbf850fb9984f94d8cb3e27b59416262ee3f84845e092e9d995',
 '6352f499d67871524d5612de87a2a405c7c6147c31f96930b247185036026a79',
 '63908805bc9e386f6e4330f505fb8dfa8bcf60922a597bf2c61b782571bab4f1',
 '641f785808e8ce13daf2b5e4bd645f30edff1b4d339078195fc084d5b69b302a',
 '645b080cc2e8182e18688f93cc08fac577c9c2c6789c24638a5ca96301d96ed9',
 '64980f072e245b96b75c9b201442d7e7aee47f8ce413f9e6836fa4dbe5a95156',
 '64cdaa7b3c4b78c11c4851289cbdd67c784e55c979be136206f29cd6f2f0683d',
 '64d7218426ec09999e77fcac25e7b3b4ab304ba863285565a406f295e053f19c',
 '658cafa8d5c90848c0d22c767b0b664e1c26a88961ce1fb65352fc1b896d4856',
 '65d4c4137c2a61a9906c89ab3f66d4e8af798886c379880b0c75d944170c81eb',
 '66210fb4ab17ef1ace087949b3a20e2cb3141d1a270cd554928e8f773e3d9187',
 '66344ab1ecd5c4629abdbdf25f00810c0c0e1e0ab90b640ad38f14976f55dc35',
 '665a346367f5a4466e2efe29a8503213e5bc0d11e0323f5711ac20898ef3c227',
 '67c42e8e30046404cf4e8eae9798138a5775578800b86a9d71df418dcd138676',
 '68537898cc830d5e83975ccc9257a958ff51a7c3713030a893db48919119c26b',
 '69df792eb31cdc3fa80f3b886ab19aeb36c08f40dc7b8a3cb30e56a9ea7a1c11',
 '6ab46d5b170935345487851b34fd311fa681d39147d50a47f04dee16b8db0e4b',
 '6ac7ac9170154bb0b4d273f145fd1b1b9de9684e771184a7df859d3a3c68c0ed',
 '6b2e25e7a5f8c814a59c7d56680eedf3e1c4b24dd1bba2ff4e8d1486970ea833',
 '6b38373513aa97477f9c10cbb35bceb09d2bcbd556cb57ad9142928fb16d1c4d',
 '6b405ec0bbbc17390ebcba5f4a19a54b9910e75b6a5b7193040c14fa090776e3',
 '6b582875e246e8c8e3a8dabd8e851bbe79755135fa97f6ea2e488e061ab14922',
 '6b616d9529230e51069af622003bb3f87b0a3017a520c0954cd9005cf79a5962',
 '6b77b9046f608fc79ddf00900bcdbb36e6f7d295b8329849f41cd5acf9a6f3cf',
 '6baa791395fa5cec0d2815bdf52886e73e864d413909f757f0d8416b981e8576',
 '6c00eecc2a0607ea759457fb97d7ecc42165802c3666a1928b932a867e6d0208',
 '6cfc6cc638dc978d9e2c2ed15ed512193084c6b181a3c7f7ccc8c2f2ef0fd774',
 '6d0512576587691118193658a8bccd840963aaa0ac23a4c5580dca531c4190c4',
 '6f3e1dd8d72394ec26117c470825afc3237e7fecb369469890285f7de98826a0',
 '6fa922abef43fed6f7d8bcdc0a433a7f3a3c1ddf065f073000b420dc5f84ddbf',
 '6fd57f2268b8a5f5a0806356e26141bbf6e53587c00c20891c12714b9a27c7fd',
 '70183a90b8ef4e5cb6ea651018c55ca92818311f7bcb08c3f10e1f0427c8aaf4',
 '705118fc920efc809f4fa44375b0c82c1b51d7bac0f5a29de024dce60cb9dae6',
 '70b96c6b2075afb7cc11bd6a6c5236e780d61b234e19d5824edaedccafbd5c7d',
 '70f2530d0e9fb55681468466af13cfac8005d12651bc1e5ad6eb3623773939ad',
 '71191e708296099abbd0a35e3b59597cbbb7ef20a195ae29f01a618174f57eef',
 '71362e26125f8371c87bc87f9a69304260079da9c2c890b6c88b859690f83ece',
 '7191a1a736fc06351c0599a4ed3c961b2a2397c3b23b561768e7d63a51776b8a',
 '71e788f9afc6a156d90dda5f70bc9f66f345bc81048c91c39b2c7c074fcbd965',
 '73105c1a28c3915514b932ea013942d95076851283234f2f1ff7ea32d079ef35',
 '741434cbfa56e7a7736d31670987ccc5ab7d120f09fc51daa53b1091b52c824d',
 '746a92fa18b54e60143b1c4a4809a5188a90a3a02e2887e3bbe8efaad9e75c0e',
 '74d9b0dff04af50ba651a1f1206c55f0bbbfe4c542fc40a416f10c352a73f21e',
 '74ddab59d09aed73939113f4a9a085620eefb4329fcc215c328fbc0c66e1c2e0',
 '74ec0de593cc8cd5f5e390c3b32204a64464e8ab145377aec67dfff29d629bfa',
 '74f129a21002229dfc1e0ece90134f0c16836c4e39d9d119b7c8ecaa9e2f1ca7',
 '7563390382a5ea2876aaeb047cd6020a335894c7fd25b371de8449dd64d96f9a',
 '7584cf26a265b11fa8b15df080a2ec53585849d90ca5675bf8a3eedd54a56f0c',
 '75c0a186901e32caafe5a734a0b360e1e18a0781cba37c60878ef5968540fe84',
 '7602c513a3e2260a258ec0bf742885fb6fbc20564897498406e79c93cb6bfb85',
 '76963795a9dfb15e01d8bcb20cb998eebe2fd49f5147092bcb87292c6ae12c79',
 '7704c0b0118f5077cb39be0eedec832016a0230082403dc30a5262e4bf5a72c5',
 '77598370981e909f1ca15c8559c5966c77d72708e735bd0ac23a4fd39b205d92',
 '77a9eb7d5083b83ec5db03c6be52ada08470acc662ff120637ecdf4f8f99173f',
 '782f13bb1e6c01796459a32366dc6a0f7f111b6804545c71310ad85f2fba682e',
 '78835ddb8b834c1b3768f455284ae32a84bcb8b7239ea311c62c07dcc4eaeade',
 '78d6a59bfe4b01b79e6e66a299cd9f49a04a38c9c15375de6f6c823af5690960',
 '78ecb077b7ce959d8d79ae79d27a891fcb16d15f669ea5e728a89d3c5948b6fe',
 '793e066adc5e96f48f87fa9baf4f752b9740f61382c3bafcd46feea9310d01de',
 '7971f2db3d8cbd025c3ddfec4c954cad61332b0615dc9fbecc2ce1313a84fe7e',
 '79a06ed0191427bc33d7abefad5c0d840ffe493bc3e6a1472e14712d7cceef36',
 '7a81f403e298937859aba7ef6124f736c9766c2bdaf495c2cd32b70c1af85998',
 '7acc0ba615a05fbd6a13cb9d7f00160b4d2e2c54b22bc02c8876c70050596f9a',
 '7b1670434dea9083a06bf54c22b7ff1e38a799f89dfaf3ae7d08d701a175c65d',
 '7b1ca0d03843172001e554071c4d967bc228dd4a5a25317bda40b2b243518ed5',
 '7d634802bc826c2712f4060466c1d0880a8125a9bb424932f75ef302b5d342b7',
 '7d69025b6b28ac07e0f7d2bc7c1c74396e5cac8a607fd45504f88646d8a9ce41',
 '7dc0f9cf87331d2d993b5cf0871d2e02da4e38d025f916ead9262726e5a2d6bc',
 '7e9b812ade6f929f60b4a89e4476897ca0ad16784abefd7a380fd46b58b2c8ed',
 '7ed1059466ea38e67dc584b67f6d0491da424a94a5346e1e3afd3cc69ececf9b',
 '7f7520fff2f53878a294c3d25c6194146ef0b6a4e8a86d66789adf4d27024f44',
 '8088d0bcf08887ec2133437d23ebcee6e012e1ddec1fe890228a8135fa5c6080',
 '80e26eede9887494a081c9524ab10df6f0cd6a26c3fc7ed5c29680f8fd4dc0e3',
 '81e36650afe8418f9881cb1312fba1afb6f8b115de4e7e37f29867842b799dfe',
 '822049006510aa2e68fad2ac27ae8b9302dfa06b49787e0fe200c23e49c4b415',
 '822341dd1ab346be985513fa05c201c518e7bd63ee995b516aff6d8b6e33409c',
 '82f04524a7fea4d26c76ef976d82c7dd6e343789724afd94490fe6ed3cd89cb5',
 '830377cd73acdb93c8aa2b8a97bdda6157539947ac6801f951f6c7fe1191b7c4',
 '8319ea6d209c6d240be800c454a9b4db11f7259395be6986d187fcec734e5782',
 '84645c7512ed8238f6b26d382d49a52e54973ea6e67cdc35019a77a94a3bfe13',
 '84fbbbd7cd326d09ea8cdb6c2dd7f2da9b912d22e490be3d695c9acc18239d0f',
 '85458093d75501bb06af4b8fc73fbdb8401dc7309cd2d35700b8267bc1b3e305',
 '857d884b78a575767f78b5990ef5194061d088b64f46832eea1c7591f7108731',
 '8648f10f5ca66bdccab2083a84666a5927b100e960e5b9d78ba05f835f75d5ae',
 '8650b37bd04ccca3dedcad45aab2eff2b986bcae99e8e7acab5e35949d427566',
 '8685593c9adfe50bb34c66339ec543c879dffb312bcaa593cacc4e43d5e83bc4',
 '86e65f943c2ffa78f49dbd608a7323b86b7f75d9b830685d65fb362b9d348379',
 '878c73f40ca16112e6897698488a1109daa69d4eccc56b953cefaccdee268fd7',
 '883a6b6aea32e970502088a3449b40756dc228608136fd1a83723b686cd228ad',
 '88916e7cf145a29573d57e021a3de566014e83192125a4b6d25d9d98f52dd6d7',
 '88d364d6de70c5a65225738dcad68d5bbcfec6a495f435ca58e829bf68e4a11c',
 '8955a394322601cb6f29ec407fa8fac2847d7f0bfd1298bce096d23d1bc71bed',
 '89a45641bfae95fe1638eb010adf92a70c6435dba04076330528a2df902976c4',
 '8a23ee5fa9b4ad5da1903f19a9116fa1707254a0fc6db059f4a42dd276b3a4be',
 '8a6330257816b2cbe95b635da6d109e4613787d13fd08dc8bb233b48f43771c0',
 '8b5b15b4f6e9e01fef5bb78ced2c37bd3ebe434eec219fbc7d5c54be7bc2b359',
 '8c03c970858617f24298a2ba9da65cc14ea7bbf66fa41854f850f533e9dcb2d3',
 '8c3ebce039de07ab17df436053915098bd7cb79b92fdc0d1717dcd7f0ceedf82',
 '8e2907783bdc4b465430528c6b950a510627921a7c2257874b3814d3ad29f404',
 '8e55eb783136e57eb83078f4fc942b95e0ac74b1ec084e9b77deb70eb68699cc',
 '902cc18b08b4f64798f1649db268e3f491519a640022df084ebf529b4e4c304e',
 '9097b4c5862956cf4efa9e36c985f501e34ab631777ed066569ee2668aa8efa0',
 '909c049a6cd586e2b519532f185f334fc85634260c6058e35e7876217ffbfe36',
 '90c8c227ece31c632cd303967d3edc4459031a4376184a250df2eb6016ac7bf8',
 '910ccc864406b84a252af5cb2dc9afc975a15066867d91382fcf6db089ea17de',
 '91397da8004cf466f4b29b67f01049c73ab032c79c4982383cb1bd449b375f6d',
 '92385cd2c1ca2538216db06231a7a8d45b4e175ef022acd675858e2704308802',
 '9265b80b5e9eacbf110a67016e154065f69ac831beca36d19012bba38a8e1f67',
 '92d009e9caece796c5669dd32fd2b076247f3a9673c38cf6a727ea1725ae6b13',
 '936f6c1689c67e06596571deeef73b6a3b085344a51908a84d0b5b264da3bb9e',
 '938d8a0bc163f5af8ef6d06fe94848fc7d382574e29e2409d101c293a5201d5a',
 '93cca77a0e2c8c9c50a563cb2a7b34ef568393710ee0f5aef25746fba1300cbf',
 '94ccfe485fd82d290f405806e6c91e071d221e2b048961b71f0cab0b0a5a5c37',
 '950247410cd9b2e1e48c0adfe3f34e469b6ba7e27f4024b024c82a12cb614a35',
 '950a6ee9e73b9c1233e6785beca853771eeebd4aec77d2071038d047595396b5',
 '954d14750c7d02a096219ec8d4da921e4b3669a0b9b1a95f1879a64dae3dd505',
 '96bcaff277e8508210488a2c49233f4c0be4add3937352c624489e3207e75e4c',
 '96f156a320745d71a70afe73d89ed1caae66fa433278f593ab8dd096002477b6',
 '974caf69d839c0aa08979433af9a2532e39db74edb82fd28f8cbe3762ec1ef0e',
 '9794a7b8930d20b32158f403768899c4d3f7658332fcf17f622fdca136d30429',
 '97b9bd65c3435bcc05dcc001b31adea7e22d5bcdfd2e0efe68e1dba40c1e6de4',
 '980541c71696fa857cd40fce5e5bd76214350b17af2c55829061fa556895c408',
 '9806867e7158116a397a24bc19e2b103b2aa73ec83cc7c765c13bdb4b7e06723',
 '9887d44fa18c7eecfa62be7b66db5067a59b84cf2984aa765251031824d95f82',
 '98f2a00b970cc1ec6051900b741c90a3a594cb1bb3e7a65eff69e2ef98f8e73a',
 '9962b4422c6a642d4f8c6002b82f2eb241c5b013c8034004ba9e7a79152ed6eb',
 '9974d9bc56c6d8c85d9b6f39a12ba91f5866ea66ea79c02aa901c7b6de959caa',
 '9a7ce8a3b2e008d8512617ac5c0c4bc095d7c349f1b2ff451b76d52934b24895',
 '9b2ac8637eec3e827647903eae767b95acf366c4dd3e472fd414d0bd04211236',
 '9c463bfd5d96070ba3becccac5117f0bec24ca60374ab07d33bfd8b1be9112a4',
 '9c76e515054b6e660d178d7d87d9df4efba750d26a6d2136f17786ebf7db63e1',
 '9d156fad4580cb242804a8f0ebd3483d12f12261212034f200f2e13508c642c6',
 '9d3db1db2e0c68902aadc22ab02da267b9bb2d4917795169756c7f01cc42dd14',
 '9d9449a44ec00290ee657ba30cc1723beb1acd0e49585d377f0e409c868824af',
 '9e8458a5b8e2b4d9f5f1c75f1b20fef162210ae837dd4719fb3c9c1caf77250d',
 '9efe464d4119ce373ba60b434fcef4b0409c05f260588b48fa3c750e1acea69d',
 '9f740fccdf0142fa1eb038e305e50e74b08cfe3dbe1164de4c124f15b01a67e0',
 'a00cddd5698f7a4088a0832d60e48f49d3f972e3080ab310d358dded07acc79c',
 'a0426299844bd50f7e4e0a56b2dda94e3a0b05414fbb06fed3824f3d5883c710',
 'a0496dd533e212e0e2915b384b6448a6dcd7240ef8b539b582d0b94e907ccf3f',
 'a19acc94f65449ab3af78d94780f5e805328cc34a8780296cb922cf77d3fa709',
 'a1ecf61d6b023444b9973cf0141c13a32a30c490c8903d701d59f34a2ffb80fc',
 'a269316ee7cb9159fe842cce14ddba61841617c93e4737f41d547a4a6d88bb7c',
 'a269bb630cb44d70c53342825b012c71b8cda908abe9d35a00bcfaecd97792df',
 'a2d392741f426ae4b8af46be15d401b189bb80e13aadd5d961ea72989f366ad0',
 'a303e49a30e161c3551e459ad105fc79dbb2839923c7a75bbacbbf5019b4cf48',
 'a35f641d78b46b9b212b24f642f3e474f8ddd452f819beea3198cb7f4e25ab7c',
 'a4050bd2fa13a516661734a159d9d8e6071806cd63c9406822636af1475996d2',
 'a40c0866c2c42655e3a36d0fbfb401144f1c069671b4a12f15a3eb700a647ffc',
 'a41d8afc23ff2bdb6313df98c0a37cfa5ee84a7f75065a0fed18ceb03a0799d2',
 'a49ff27b1079d8c72e5cceef06f7762a6c639dd9afc0ed798288082d16cd8fb6',
 'a4a64a222e75f313323e2738c09c3091822ad853717d94cdd629e9bac3244f1b',
 'a50d3fa370a2c8864795cc8008794b6d614d85594aff7b180e023a51864395ae',
 'a58fdfb7937a1d9d40459d337078c0d6e353d6f20e1582dcfe302bcd010ca80f',
 'a5ae39c2f87b9ba3eb78a0a5b6c2dd014aad954f2e276c696d6c669a8cc0cf37',
 'a5c87da68f9552b100c4b12f4df2225688a1f69b693c6f0193c4f37294206dd1',
 'a604ffeefadb05dc8b9b60e02e4d5a5e0adfbe4f2c4215366abd88ebc4f229a8',
 'a773176935a8666e7425b076d71ba69f1247a3d2a28fcce91a7a5f02c9a599b6',
 'a811c62a57f9dd1d71119394724953049c459b9a96f873d74e5d228a18b3fea0',
 'a81b8d96aabd01ead9e24d2eec3695f61a6c4b32fa427c9e4e0ea2da222cb7f4',
 'a8306cc4f1cac93294af1024d41e946bd32089cd6a75edba7486a9d1e11eb5c7',
 'a8482ab8c8df2d6ef0b36bcdda4fd858002def9aba27a678d6036998c728af1c',
 'a8a4eebd0ccfed144fe6ad13e3ffbb9f6e9d570499c1f168b81619c1912e630f',
 'a96be0126a48b00f91ddec3c3ec535b704408e65835fa64ba923d1f9fae4d03d',
 'a9d5705cacbb9443ba458e8b3398600b668c4a187e5678ceaf841ead6f93e076',
 'aa85a0c2c28fc0687e518005f31fa8ab398ea8dab8c0c17311be58535db8aab3',
 'aa86498107b416947444e170953411550f8970e4f89c7670f2f5ebd030fc803e',
 'aafddb9ad1ff1712f08a3b3c24da0514e2d13cd002dd4d0099115e4a49315b29',
 'ac18534dee0db2ab49e8e16c5fc52ca0f2a356cb7cf47b4e53a3627636b6c79c',
 'aca0c8a5519513ed367ddf24e898b84c1e45211a806d6f4bda3a7b3b73f0e006',
 'aceae285f1f13bc613d45f104f31d2680feca0e6abe87cbd164cd2f5b91e8869',
 'ad54eea37fbef834006a69bdd1d06ada516ea7502270e56e429c41af6c850a2f',
 'adb2288d122125ea0fd78631225ed06d132365895791ad802fb7142635d37396',
 'ae12bed1afad6107c085caf6a18edc7a3f384d0e12bf8101b4f339406f5b31eb',
 'ae2c0bbdefbd08931480e633627a7e264d3aa6bb50dd9802ca446661056a45b7',
 'ae748d36c3d6eb9f9d684afa0e92d6634d22368b56cc3deef14227eff372707d',
 'aebbdc66b01d9a97e598e2633069a80c11dbbc4ef6cae6803afd891a72c5860c',
 'af5ab8d5b5ff7e1b5c0ff50ec5243bf62676723963ca858658cc9e635ac8ffdc',
 'afe490e5be879026bef81d5990432e975c89b80991c8e83a54bbc92b2ce40bef',
 'b014dc1b2caab1f78e6ac0ea822379372fa6df8f90508f2c6285606be4ab7c83',
 'b01c23960956527a212659105915c56a26535c64f31e1751b2ea78d9283e92cd',
 'b021ceecbb6fcdb28fda75d3c6fb75eda8aebf8ec3872800c73ee26acc6c0b0b',
 'b0b8a53115e2417aa3c84ca42c77e88d9f17d7e67bb0032f3d8a07b72d7311c8',
 'b101da6d7102601fb26d7bcfa010076dc1ad32314ec365ad384055d40505c112',
 'b247d1ad5be32feac897eeb44bf96a45dfe6b64a0a9ff69f09d792f703c89b9a',
 'b24f2c2c1cc90e7610278e404c9abea27d2bc2d38c329ffdd58b2ab40285e374',
 'b30815020c0053f2cfbf6e8fe8537a5cad6772f469d84dc81a4ed95420c30513',
 'b60bae94a133fdf06bd1aad0274b4d175f0299c4e4cfaf2bda45cfb51f8ab73a',
 'b617e2ad790cf0cc0f0d936918ce3fb080157da211740cde637719e03a97e360',
 'b70be3eab6b41f80bfa47ec5516ba7f4a1e006d8d7a78414ebce3fec48aece9e',
 'b756f8ddef3899114383726e7634e9bca9f6dd3f7c72b44c0fc34e0eab66a075',
 'b75ffcdb7a51effd19f2280428d7628a6a3debd9719d9efbecf02a027ac1a397',
 'b7f27b4cdbf0d10906587e17d29d58292147446037df9dae25575fc281d43c01',
 'b7f5a49f53abb9341461db52ce97fc6a3f7f38cb54165178d6b2cae4d184e0a6',
 'b8fee5b0f43bd9b83d0cff5f9d1abcd2485ef6e5775ca1a592500aaa18feb722',
 'b99bb55f1769ec4925dadf26a33c3cfaf331b9152e4fcd8d5c5003aac1217d0e',
 'ba720fb6c2b8ef069949b00c780ddef3fd24b3aac356d381d568dff102933680',
 'ba7d90cc80e8b326dee8cdc0bb14d03a2515e1c90317cc6750973adf0b42e7d4',
 'bac9c1f75d0ffebe2691bc3fbd5ca812885f035d80f857a6afeccb8860601806',
 'bb90ad9bc4b5a17c270fcf6461b42623dbdcaf8b2baf14822410a05278250a98',
 'bbde28d63de1fe2a3ff7d4ba2d89bae182940d83367c00f59ad6623674e26739',
 'bbf8081f5ccd7a1716fd797c58b436887cc49d9f923fbd8c4b61bec39f26bb78',
 'bbfc6e9711d1e60402cc15b59b0bfe7ed1574ea0d4c08618904e0b4234ab2a01',
 'bc2aa368c4d3748b6da8112916ddb614eb4bc2d5b24d3af45910cb3b6101ca74',
 'bcfd6ce1aa199950ac2fb0f47837ae7630cb4f371438bac8f346a2eb78b8b1fd',
 'bd2edd5f3079ddc90159db9f500babeefc84bd62197f67561535e065c96b8bba',
 'bd5e816af770c636ad4331b6563e561fe4713d71ddf291d670a92c1f9d717fa4',
 'bd9a6de3c2bb24f4bae1c27183f11585caefa49e0bd35366647338ec708f3878',
 'bdd61d341027dd2fe354bad83d163afce324715cb0183420c8216276677d5ab7',
 'be0340a5ef34d0f7d2728e7626eacc40a325672f9a6a07c27ad623214281a147',
 'bec2f5d39b10f739b20226004dde15fa4117e89c21af4445ab647aa35b51d424',
 'bfbc7c26998689f1f0e51b9a578c1618b1618c7c753df02aafdb4cc80a62c30f',
 'bfe140e3eb2dc934d47ed050e1b3b4a576be59b4f5ccc8070ea33e7439b8145b',
 'c0d7a08bf3350d29995b2d8d5a59cdcaac67b8c3c376da3e27c69a30ff0353be',
 'c14876a13ddd0a2827a20ca4e582a738393f28e3ec7954c0151aa7ecd641d6ab',
 'c16b299fc3e664415b00d39396e79e76351f11276efa048dbc93de7099893ed0',
 'c38ee1d0bcddf5df2bf57905a587a054539e42ec3a836c95e9ea7ab3d4f0daec',
 'c3ddd48c4551f0c33dfd729c82845fcebbc50cfd1d34d5f258dd79b567ec03b0',
 'c4131e8b9b4ed7616297f54b902ebb74ee5579efcf9d695d805d4b2974e5b147',
 'c4c2771622ae2d19ecc58f549f73cf97de79bf997d0e53a40eded30ffe1edb61',
 'c580e4ba8871eeeabdef60d44b43c7e3c3f09be9a31f0748d1212b53549a9690',
 'c7374d646793947ce7ad801c07bcc5abb4a99981b09ddb4c9023c88ada8a39a8',
 'c77337fd8f221306cd59121e367bdffe356f373d7a1d0c346f63455d20d11e81',
 'c77539483a73102777c416f71b02f8adaf41f1e92ee8b02033fb622c3aafa021',
 'c7a3acd3c1629cd896f8d455a448defce5d4ba141472cd65ddbe57acb00ebfb6',
 'c8590acfa54e5dcbfb3ccdff978a66597a1e5af96ecac11a53f3f0da1ccc2931',
 'c94689865a16ea0f360d14a6200e0a57af6d51c38dd21428e35fc9f6651c415b',
 'c94c7260b6db7d51f70c36567b75452c4ef5348596dc42ab30ee69d1fbdd998e',
 'ca11e5f7f7fd55121ea0cb2dc1adfe10163e80dec7a7409df279a5f42f85090f',
 'cae859aa86e10655571b2540f635bca86c246ef4e779d4d88a5e46a0c350d658',
 'cb64eda8cfaddb8fe936217be4ef1164e6cd9079e81f96c4bb4d9df519693a5b',
 'cba3e972e526fc3cd95471d04f5e6b8af1854001b97612d7a3c47fd054534de8',
 'cbc549980425c0cee625c101c81eb8c61afb72b646537793c55fc8e96a5a0b55',
 'cc1d524d47336f999ef2ea7542f4186616ea18e58eb723e91ccea46bb2aafb97',
 'cc5f4d6f0f18ccabb8508b02cf8d5f19d6084b306832f4db3fc4b4fcb7ee8217',
 'cc664b82963376d9cf2a337a36da794191dcb5ef2ee6d4499c7333b1dc790847',
 'cc688e677724841cb3e90c8e8cb77142b795b204effad38735277da9ced9a9ec',
 'cc6b146df5769756ddaab3b5190141c065450fde2ca0079eb46d9f75d870111a',
 'ccfba22a3d3c08cbc9aa1f8c8bf9cf9cef77d979ed34ffaf4b29eb1271c48536',
 'cd148901969f7839707722cba9eb7a8a8bdce61a052e905fc358f2cb78708244',
 'cdb84f759e505222a8931f779a143958226ae49c4129f96548e32e5f2ec3a016',
 'cdc2c359aedbb3f9044e5cf8d3c26ca85c088af056fa9222bb0cf5b9b978f9b7',
 'ce3a6679750182174308ec94abb25ba96202077de1f74829666782bc3c754778',
 'cf5aaeb782dab434172f104d2b7d2fb0125bbe4e3b46dc15416f4c42eac3be7b',
 'cf5ac2a51082ee76d7deb37143b0c9eabfd9b37aaad9b0a6d6006e8b0cd07af1',
 'cfcaa59cd51df080b344dad1ef45c198bd77a5385251f548331399840d2ee3a7',
 'cfcbcb451bd11a97c910a7ea88b6200cd78acea51af188fea8ee19856fe0a8cb',
 'd0fc354d84bb450e45f11e3a235166908f520360de156b33cdf9b73f5b0381f2',
 'd1340e1d6aa88461f8216ebda114f5813450b702f8c17dee9b8add88245ffec7',
 'd32523a1128bd269a53c55b647e86dccf5065ce112f054673213b5994a0a66d1',
 'd340407bf7d7421f420d4f37eac7d85ea1a0dbf4f2df9480b4d38a5e93a40d9a',
 'd35fd8579ed3ca0f4821a83221a196497aa6a7a60b2aa9cdb8a7df93414913b1',
 'd372d45e3ca3d9f2c56cda98f0b7824f150d8b7f1ea397015217b91233bd564c',
 'd3aabc09fc2b44fa2e14d3bd5f276b47c009dc8ebbac60e93ff4d2e713a72a5a',
 'd3f6ab78e9211e1e5851a7bc304d3d537755f7416bb18387147aabc64db18385',
 'd40df4bf56a336db493c7e4e3b0ed032b0f91be6f1236482dc6f3c96127a7aa3',
 'd460e606e44ac547f58b1203998bbcda56f42e0f01da1a562a84c8e4de42ca91',
 'd46dee46d23237c93e40798e25362b9ea289cfc88470809208270b5d6c00439c',
 'd50f1b8c355aca0a324b50cda4bbcbd21daf3079bbb0dfa54aca14ef990eff86',
 'd558c98cd78ad5bb88d3663544f28345b450a558adb755638be5e9a6bbd26d8b',
 'd5679ac10b016ee803cde63ca7f428c599189c82b28050db82739796d222cb38',
 'd5c86adfd9bcf9d4364dfd8afee140a66cc6fe07db3ca31a85f1f7c9ed32f708',
 'd65ac837686942510cd7bb9bea6d522c10ecbe18a465923a5b83c64b3e73073a',
 'd694748d05c3dd292c505ba840d5e16ec8e739f9b94f1f7a7dd858557f81c12f',
 'd743a23940f502e86d3052ed6e024359f539ec57a34cfa05d08952cd630df14b',
 'd763d4bb7fa44f93db4e0fa97d2a15abccb2f7cb0be0b4e9362c61cafad5fb49',
 'd7850935fe6f44aef695805313f336183396bb6e72b9a09f55c9450eba59542f',
 'd81d7ba47065406b000872159356db3857b9678e633a03407912f80c2a4a7320',
 'd83907d9bbfc2197c0381ab073ece2c08744669fbc9117211f9459914c032733',
 'da6e597ae2642072b818c2655084a3cc9426d9f8910733dee4424a7880b3c5e9',
 'da8acbd4a4a53880f687ab0d59dbee8e4eb0a2f3a572c19a2e796e6176a1badc',
 'daa56b5c952c53d8783bb98e9e1612e1d05577afab35addd3c228e8d89cda93f',
 'db65fbd69cb086c55fed034e74235848ee9906cb1e90735d67a448b107c4dad3',
 'db876a4275a981d157735fbcfb47de608524b084aad4a198e771986679444c8c',
 'dbac74c8b6d87d8669250087041dafff4dff2a3c52841d7a7038cb52adbee8f9',
 'dbb91e1c42ab93417e7c22fd67055425865ef3b327362beacc845755eb5cee89',
 'dbdbdee5dff98892ac53a11ca7fa215e83f9140ea8f0333fc15ce1313a7ee421',
 'dc855f33a8de50f1b1f733449158e61551d3b2227aadba034af86f38c0efa875',
 'dcf35cb779551b4086099b9f4ffebc1d42e0766a07c7c19dc1304248a21da6fe',
 'dd0436750e76e7a4ce9d43651b56eb3ad6061418bf9eb71db97303ff3357974a',
 'dd443a37065e7373e704f12fef800a2f70d4bb684cb6c4cfa8e54a5e32e149a0',
 'ddc370f1121d18d79375325a353f4ac38241846967e5deb567daff395dfe9b24',
 'de55d013a301cca286cbaadaacfbc1d282cf2e2394d5cf8a53453e59db42cdbf',
 'de7c137116c63de998d97e94416c18d17d57ad52c8bffe6a4bf451aff95ea32b',
 'de9661e5d48cc8304afb3d7e9ee78987fdab91c6d07600dd22736f79550c6c6c',
 'deb49272726e23b04f1e96e6ee82713495915d76903ce0180608abb9b9c1fe50',
 'deba6b4370bcde085c85b3cbea4f869decff59530a96b1f302d3e1c7789be09c',
 'df225872961f9588e6d90b8627638833be7a1d406e862aad7f1e705a43c7cf91',
 'df8ab86223833968feda388a1c19cb0cc0713eff8aedf84938cf05692727bd62',
 'dfc617feba7cc6f2b8c49c7eaab23685419713231951ae7d36d61d3a79249084',
 'e1990a0302c94521bdc885546adb3634c63f825b0075a604e27d6dd60923c708',
 'e2f0cca4a36c32182ef8a49e9a14203948c94440cf0f33dc50261bce3b2dd134',
 'e3937bbf4a1dc8892342d826c224b7d9cc55dbaef1cf740e0921f3fb701b7a37',
 'e3b1625f9cb9d53f01668d0766d7cb9c6f09171d3b784163abdf90199dc752eb',
 'e45bd0652477c641a84893c9bacb657a7b379bce5053ed235f35752979c1f06d',
 'e49643d9a8fc9556468cacb9fa2c66705724751659835c1ba0708827c72d238f',
 'e610753e8c717c5defeca551752afc868a45788f3188a86a828fd0364c591ef5',
 'e6b1dfbff45d3706c1c684415a8b0793b06ec768038f3a3f334f7a017346838c',
 'e71f68df10ac31b5440ca542c08f4c10bb1d1e34291a581e5fc97595d3b23c38',
 'e834fd3bf3514546ee88315eb2ef827263f1db107bcd58aac1851524f7d8f3de',
 'e861e37856ce90920b7a07724176f7fa10d8baf13fe0999ac33c9b4cfb6920f6',
 'e8b3bc30d6921146f55e7941b6510bc3810771006a4b77c568eaede1c99975fd',
 'e909abc527f61d6570467a097a83e1a4cf248dcd636fd31ff92cdb5ca5990b9b',
 'e9d64be01d5098b63e9fddae317fb80194747cebf085cbdc4f31c346359d190b',
 'e9dd263bfba0c2992d8086a498af3ba1f073ee1db3cb5c153a8fa7fd76530ca3',
 'ea259608b2935a026b488485b8e5be94c6af23edf2cdcf5145e0ef8ebd7399e5',
 'ea52afa5c359184107c0ee8e8ded0a8412b994f2dff07b0289b08a821ed4e4e6',
 'ea858709b42b9055d7a3cc170261883eaca0869c5cdb544074700a59ba266f50',
 'eb3bb445876d23b9f1c91a7d2e1e65272e802ae4703b44b5d84722fd6930fd77',
 'ec5186ece335011dc10ccc6e82f5a5eb318771f116072d17179d7236e62a54a5',
 'ec978216f4ca27eb3fef6e24625f3214690aa5d8ac0b8d07a188d3c443a8c940',
 'ec9f7e6175cc70ce4718d91d7a0775119b8e7e01c4c21b78c1b04633c267e556',
 'eca0cf6493700ab2de9a2fddee2b504e11c24b7a05a43e42382d704615c37f50',
 'ed44a0f440e9fba596cc9224330919f4dac20c7267ceb1e7eaa19cdf8380e9f3',
 'ed92ab1dae5f4750dcda854d545f146f8e9e96805baf47ab5e70e60c07c14cde',
 'eda43adc38e801ac493a703f9aef01340c3e017f42e8cbd90049201f0425be97',
 'ef1e38596de97e366cf71f4fc367bba75f49c92a1c660ee98a960fe55a8bc858',
 'ef5551f3148eb4111ab74695a8f80211f0535f2e0529cfdd501ebee328af48b8',
 'f028157769f3113f1900d1d3a2f9e241caf6bc01301bf726590771617d59193f',
 'f03c2202984eb5728ed7c45815e75c85ef4f7be34aaefa1e8d577391a1595d99',
 'f07bcc437c95972506fbea960f11bcd2cf5745c848ad28fdc1b38df308b895a0',
 'f090ff1fb9efa4f0b17e0d5246301f1aa711f811993f6cf1b3268b78534f7349',
 'f195d05876f4d6d91a895e0f3dae2313c992e7936d246c93294274ff3829e574',
 'f1d134d11d25181a500faad72d4a6eb952df950a767d239d6ec58dc9fe212802',
 'f2181ad6beb06a4c3d95c4d6ad1a9245694ca7bd20dd10309bb9ef3961ed0c3c',
 'f2376becd6326a461465fb86c62c9b08de1c5ba0fb629994743a27d70983b011',
 'f2720db428d58a057dcd4d17053b113bd9be99f15a6649cd09e6f555bf875499',
 'f29c3fac69375dcd75461261139c9a794ae9670b9d612796a64f3ac9eb471aa0',
 'f2bad3e35b28ffef0f0b76397798a0645f7d104192c5af21b43fd4795a5460ce',
 'f2bd6b3a8dab18ddf3367bfeae13d3c1b62cdbad516c3508a7c0aa1e50c304d2',
 'f343312fb08b6e89ecf1e85abfce3e3ba86340e9ae0dadebff02c52e09d19795',
 'f347e27e44565e73aebf8e7f0f3f60e655c25ba0ddc84b1efb5f6b1883283ef6',
 'f3d9691a98211e40bf4ab854305a776e647fe01cdf4a3e74e3c108f3a490c46d',
 'f48c0818be69da0cc9fe79f739755771f2c4ffc75e01558f8eb6bfc11c0d8db6',
 'f4dcd6d3784a0568b0549705fd19b07ade0c1caaa90218d9af3513882a1b02a2',
 'f54d0d8380405696d728bbfc122e4c927a9f916025615dd022d091216650093e',
 'f6388d566816300e196c68354162cd9677cd57fee08028cadd35eb5ca45ec5d1',
 'f65e8d64618f0bad320fd805efca56823d74c833bb66a33fd6ba18a23d159e1a',
 'f696d41be1f9ce0e97b15259320df4e5c82d79e8df77c7f0e52df831a66f1c31',
 'f73a73a0df9ab7f7a3c8bfadf5eeff6b5b7768385c25193ccebbe47e3bf26220',
 'f8066925a5a79084bc1f8d5ccf3e338dca42bb38dfe67beb01223be98ceed15f',
 'f9673eead7165668058171e2bd9f39931fbccd14c98e6417b81769deb9c45b34',
 'f982067394abc0a021304e48527d36c2f68267a54114ffe018027eb3ed0c6765',
 'f9bafdf790595a909604cbab2ee3366761d4c63afbbb17b03a64cefdb5943e09',
 'f9c862a6534ee07bfc3611c5f72ff592bf4a437bbf8b703943e88612726f8ad5',
 'fa16461d7568cb1486614b9ab4ef7b98df17df30b735f88b3b8696ead18f0b09',
 'faf06de8044dd17bf2074616b877db8585c3b0ed981d24d9bec28a6b33a7a97b',
 'fb4b489a385e7649fa2e12ed826614d0ff1aee12ad3e00113ed4a6df63c1f162',
 'fbc3e552422bc72e9187f1c5a5634c3cb9048883d03a82392a8ce63b6f19c08f',
 'fbfb91588c76f936fda9c7aa7b6443de330c6f33f1e18b9ab6d2b61eb667fb82',
 'fc3779e1fef9043c0cdc07134fcc7d1ca56a1a5a59fac90034a9d6aac322de9b',
 'fc92f63e416050151e401cac790b38805e0f905e57d7f8170547eca887386a2f',
 'fca32d1c407eb34a4ac28d8856bb39b9383606b768ed4ad4fe29905855185b30',
 'fd4d40debe86f77547286f2136249d2ee6277c27208934581ef146e86d797c3d',
 'fea339929c2e1dd979b21887eac81439bc9d3e62020f3d8bad705c9f816c1ebc',
 'ff00fa4832bf78c0884b22bdf296cac9db34532c38dde5562b5c2e09ad87bc33',
 'ff5862113a7fba3c0192d69b9e2fc806c0a5035ee528789c22062ba3f0586e9d',
 'ffe8dc35f241d6027b6c4c3f81727914f8cc2f5baa2d53e6d27de3375beeab63'))
STATUS_RECORD_PROVIDER_HASHES = frozenset(('0308379d78e3d225fc049c0137b7e751de95dbea577761dd318c35748bbc641e',
 '07d1c9cea7a89550471445bf59d554123e4f8ae92105c0b08b7160b7350f17b2',
 '07fae636b724a020e829c78563bd45f32b4a11427486ca45733b8b0db8cee5f5',
 '08697a5c912278dcfebc00078e7c2cf750fcc6976e2d821a1368ddead5aff0d9',
 '08d9c7ccd7cc18aedf126b637782b6edf650ce353e9bff026b49d95d5ac18ccc',
 '147d4997a87155fb16a2196c64b2f2953aabc5be4cbe625e275b4efdce335c83',
 '193d0d994be94b05824c8407749f23e4449df9df4c5fb803f60dad2b848c115f',
 '1bc2052b6ab6bf40388fc0aed45b12b5b020b10c17a5342a489f63b2c4b917cd',
 '1ca88a62491deb1a8731dfc7ecefc03e2f098f4d158c32de78aded555b613c83',
 '1dd56d6415da0f6a093efdcde26ac9a523d710cd30af92aa5d25446cf8ce606f',
 '1f80f71c5236138d756f3bcf798530a612e795e8bff93d6b52819d2c1634c154',
 '20e2d451b0b75d211f1d23946f3af19d7f8183d7af02760abe0a32c1e7d8bcf8',
 '237fc8fad85c770b25a920a0cd00859d6537c36d7232ec1cf66a4e505f6b4ead',
 '291e8fb5d52f3e2a9f81303f419a2e6885350c07144668fc38fcb2b7f2a4da06',
 '2c713f08f3d2a533a4fb49b1e43bb0468aabe162b10c06182011b3bd5887558d',
 '2d3841181bad1695821644da0c7113cff42a547fce845830f144592e1f4fa165',
 '336f2e7c57805d34a545d39f0f37406ef3fb5b93a622324b4f8e44c05f8dc69e',
 '337004d115bf3c7a1c7a3ec1fbcc886a9e234250c8b2da71f3fc1d038109779f',
 '43d01074e1456b8466bccf5472d2b662dde342f2e55b69bcf3934bf877dad058',
 '4a8d5ea5ad267584a825ad2cf2ab2510164b97958a1c9bb5bf3d8121f7e5faad',
 '4ad77e0fb41f3fcc6b1ba79b526ddbe84c4ab4f49a03b3821344531e32f893d5',
 '4f220e1d9c1b7e77e543e162ca8182a785a16e2211b3d34e5f10c20e189ab3b6',
 '54b43be97ddcd0deba46da56f7f7d952fdbf1fc27f5fe282909839bf95e06214',
 '56294cf81d120787397ece064a2c31b341a5e023882a43ffabba935742dd5d2d',
 '5b286e74ce9ec94a3ce6a15a1e1c0239fc4ece7e48dd221d04bc31cc3725225a',
 '61a3ee341980fca94bd915a4cc4274657e0c8c643669018f56914941e2a2d49d',
 '61de59729d0401c1ef13a83cf170a1dd65212aa155f0dbce9f91c0642939e58d',
 '6329dc6e1d333bbf850fb9984f94d8cb3e27b59416262ee3f84845e092e9d995',
 '66210fb4ab17ef1ace087949b3a20e2cb3141d1a270cd554928e8f773e3d9187',
 '6ac7ac9170154bb0b4d273f145fd1b1b9de9684e771184a7df859d3a3c68c0ed',
 '6b38373513aa97477f9c10cbb35bceb09d2bcbd556cb57ad9142928fb16d1c4d',
 '6b77b9046f608fc79ddf00900bcdbb36e6f7d295b8329849f41cd5acf9a6f3cf',
 '6cfc6cc638dc978d9e2c2ed15ed512193084c6b181a3c7f7ccc8c2f2ef0fd774',
 '6d0512576587691118193658a8bccd840963aaa0ac23a4c5580dca531c4190c4',
 '70b96c6b2075afb7cc11bd6a6c5236e780d61b234e19d5824edaedccafbd5c7d',
 '70f2530d0e9fb55681468466af13cfac8005d12651bc1e5ad6eb3623773939ad',
 '78ecb077b7ce959d8d79ae79d27a891fcb16d15f669ea5e728a89d3c5948b6fe',
 '7d69025b6b28ac07e0f7d2bc7c1c74396e5cac8a607fd45504f88646d8a9ce41',
 '80e26eede9887494a081c9524ab10df6f0cd6a26c3fc7ed5c29680f8fd4dc0e3',
 '8319ea6d209c6d240be800c454a9b4db11f7259395be6986d187fcec734e5782',
 '8650b37bd04ccca3dedcad45aab2eff2b986bcae99e8e7acab5e35949d427566',
 '878c73f40ca16112e6897698488a1109daa69d4eccc56b953cefaccdee268fd7',
 '8c03c970858617f24298a2ba9da65cc14ea7bbf66fa41854f850f533e9dcb2d3',
 '8c3ebce039de07ab17df436053915098bd7cb79b92fdc0d1717dcd7f0ceedf82',
 '8e55eb783136e57eb83078f4fc942b95e0ac74b1ec084e9b77deb70eb68699cc',
 '910ccc864406b84a252af5cb2dc9afc975a15066867d91382fcf6db089ea17de',
 '92385cd2c1ca2538216db06231a7a8d45b4e175ef022acd675858e2704308802',
 '9265b80b5e9eacbf110a67016e154065f69ac831beca36d19012bba38a8e1f67',
 '96f156a320745d71a70afe73d89ed1caae66fa433278f593ab8dd096002477b6',
 '980541c71696fa857cd40fce5e5bd76214350b17af2c55829061fa556895c408',
 '9806867e7158116a397a24bc19e2b103b2aa73ec83cc7c765c13bdb4b7e06723',
 '9962b4422c6a642d4f8c6002b82f2eb241c5b013c8034004ba9e7a79152ed6eb',
 '9c463bfd5d96070ba3becccac5117f0bec24ca60374ab07d33bfd8b1be9112a4',
 '9c76e515054b6e660d178d7d87d9df4efba750d26a6d2136f17786ebf7db63e1',
 '9d156fad4580cb242804a8f0ebd3483d12f12261212034f200f2e13508c642c6',
 '9f740fccdf0142fa1eb038e305e50e74b08cfe3dbe1164de4c124f15b01a67e0',
 'a269316ee7cb9159fe842cce14ddba61841617c93e4737f41d547a4a6d88bb7c',
 'a303e49a30e161c3551e459ad105fc79dbb2839923c7a75bbacbbf5019b4cf48',
 'aa85a0c2c28fc0687e518005f31fa8ab398ea8dab8c0c17311be58535db8aab3',
 'aceae285f1f13bc613d45f104f31d2680feca0e6abe87cbd164cd2f5b91e8869',
 'adb2288d122125ea0fd78631225ed06d132365895791ad802fb7142635d37396',
 'b247d1ad5be32feac897eeb44bf96a45dfe6b64a0a9ff69f09d792f703c89b9a',
 'b8fee5b0f43bd9b83d0cff5f9d1abcd2485ef6e5775ca1a592500aaa18feb722',
 'bcfd6ce1aa199950ac2fb0f47837ae7630cb4f371438bac8f346a2eb78b8b1fd',
 'be0340a5ef34d0f7d2728e7626eacc40a325672f9a6a07c27ad623214281a147',
 'ca11e5f7f7fd55121ea0cb2dc1adfe10163e80dec7a7409df279a5f42f85090f',
 'cc5f4d6f0f18ccabb8508b02cf8d5f19d6084b306832f4db3fc4b4fcb7ee8217',
 'ce3a6679750182174308ec94abb25ba96202077de1f74829666782bc3c754778',
 'cf5ac2a51082ee76d7deb37143b0c9eabfd9b37aaad9b0a6d6006e8b0cd07af1',
 'd32523a1128bd269a53c55b647e86dccf5065ce112f054673213b5994a0a66d1',
 'd35fd8579ed3ca0f4821a83221a196497aa6a7a60b2aa9cdb8a7df93414913b1',
 'd3aabc09fc2b44fa2e14d3bd5f276b47c009dc8ebbac60e93ff4d2e713a72a5a',
 'd3f6ab78e9211e1e5851a7bc304d3d537755f7416bb18387147aabc64db18385',
 'd40df4bf56a336db493c7e4e3b0ed032b0f91be6f1236482dc6f3c96127a7aa3',
 'd81d7ba47065406b000872159356db3857b9678e633a03407912f80c2a4a7320',
 'de9661e5d48cc8304afb3d7e9ee78987fdab91c6d07600dd22736f79550c6c6c',
 'e2f0cca4a36c32182ef8a49e9a14203948c94440cf0f33dc50261bce3b2dd134',
 'e3b1625f9cb9d53f01668d0766d7cb9c6f09171d3b784163abdf90199dc752eb',
 'e45bd0652477c641a84893c9bacb657a7b379bce5053ed235f35752979c1f06d',
 'e834fd3bf3514546ee88315eb2ef827263f1db107bcd58aac1851524f7d8f3de',
 'e909abc527f61d6570467a097a83e1a4cf248dcd636fd31ff92cdb5ca5990b9b',
 'ea259608b2935a026b488485b8e5be94c6af23edf2cdcf5145e0ef8ebd7399e5',
 'eb3bb445876d23b9f1c91a7d2e1e65272e802ae4703b44b5d84722fd6930fd77',
 'ed92ab1dae5f4750dcda854d545f146f8e9e96805baf47ab5e70e60c07c14cde',
 'f347e27e44565e73aebf8e7f0f3f60e655c25ba0ddc84b1efb5f6b1883283ef6',
 'f54d0d8380405696d728bbfc122e4c927a9f916025615dd022d091216650093e',
 'f9bafdf790595a909604cbab2ee3366761d4c63afbbb17b03a64cefdb5943e09'))


class _StatusJsonNumber(str):
    """A JSON number token, distinct from a JSON string with the same text."""


def _status_json_loads(raw):
    def unique(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate status owner JSON key')
            result[key] = value
        return result

    def invalid(value):
        raise ValueError('non-JSON status owner number')

    return json.loads(raw, parse_int=_StatusJsonNumber, parse_float=_StatusJsonNumber,
                      parse_constant=invalid, object_pairs_hook=unique)


def _status_integer(value):
    if type(value) is int and value >= 0:
        return value
    if isinstance(value, _StatusJsonNumber) and re.fullmatch(r'0|[1-9][0-9]*', value):
        return int(value)
    raise ValueError('status byte recipe requires a nonnegative integer')


def _status_identity(source):
    identity = source['identity']
    if (not isinstance(identity, dict) or set(identity) != {'git_blob', 'sha256', 'bytes'}
            or type(identity['git_blob']) is not str
            or type(identity['sha256']) is not str
            or not re.fullmatch('[0-9a-f]{40}', identity['git_blob'])
            or not re.fullmatch('[0-9a-f]{64}', identity['sha256'])):
        raise ValueError('status original byte identity differs')
    return identity['git_blob'], identity['sha256'], _status_integer(identity['bytes'])


def _status_render(value, style):
    if (not isinstance(style, dict)
            or set(style) != {'indent', 'compact', 'ensure_ascii', 'trailing'}
            or type(style['compact']) is not bool or type(style['ensure_ascii']) is not bool
            or type(style['trailing']) is not str
            or any(character not in ' \t\r\n' for character in style['trailing'])):
        raise ValueError('status byte rendering style differs')
    indent = None if style['indent'] is None else _status_integer(style['indent'])
    if indent is not None and indent > 16:
        raise ValueError('status byte rendering indentation exceeds the finite style')
    active = set()

    def render(item, level=0):
        if isinstance(item, _StatusJsonNumber):
            if not re.fullmatch(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?', item):
                raise ValueError('invalid preserved JSON number token')
            return str(item)
        if item is None:
            return 'null'
        if item is True:
            return 'true'
        if item is False:
            return 'false'
        if type(item) is str:
            return json.dumps(item, ensure_ascii=style['ensure_ascii'])
        if type(item) not in (dict, list) or id(item) in active:
            raise ValueError('invalid or cyclic status typed value')
        active.add(id(item))
        try:
            if not item:
                return '{}' if isinstance(item, dict) else '[]'
            if isinstance(item, dict) and any(type(key) is not str for key in item):
                raise ValueError('status object keys must be strings')
            if indent is None:
                comma, colon = (',', ':') if style['compact'] else (', ', ': ')
                if isinstance(item, dict):
                    return '{' + comma.join(render(key) + colon + render(child)
                                            for key, child in item.items()) + '}'
                return '[' + comma.join(render(child) for child in item) + ']'
            padding, closing = ' ' * indent * (level + 1), ' ' * indent * level
            if isinstance(item, dict):
                return '{\n' + ',\n'.join(padding + render(key) + ': ' + render(child, level + 1)
                                          for key, child in item.items()) + '\n' + closing + '}'
            return '[\n' + ',\n'.join(padding + render(child, level + 1)
                                      for child in item) + '\n' + closing + ']'
        finally:
            active.remove(id(item))

    return (render(value) + style['trailing']).encode('utf-8')


def _status_decode_body(source, values):
    """Restore one inert v3 source; no source code, path or command is followed."""
    active = set()

    def reconstruct(node):
        if not isinstance(node, dict) or len(node) != 1 or id(node) in active:
            raise ValueError('invalid or cyclic status reconstruction node')
        active.add(id(node))
        try:
            if 'value_id' in node:
                name = node['value_id']
                if (type(name) is not str or not re.fullmatch(r'V[0-9]{6}', name)
                        or name not in values):
                    raise ValueError('unknown status typed value')
                return values[name]
            if 'array' in node and isinstance(node['array'], list):
                return [reconstruct(child) for child in node['array']]
            if 'object' in node and isinstance(node['object'], list):
                result = {}
                for pair in node['object']:
                    if (not isinstance(pair, list) or len(pair) != 2
                            or type(pair[0]) is not str or pair[0] in result):
                        raise ValueError('duplicate or invalid status reconstruction key')
                    result[pair[0]] = reconstruct(pair[1])
                return result
            raise ValueError('unknown status reconstruction node')
        finally:
            active.remove(id(node))

    try:
        blob, identity, size = _status_identity(source)
        tree = reconstruct(source['root'])
        recipe = source['raw_byte_reconstruction']
        if (not isinstance(recipe, dict)
                or set(recipe) != {'schema', 'style', 'base_render_sha256', 'format_edits'}
                or recipe['schema'] != 'typed-json-original-byte-recipe-v1'
                or type(recipe['base_render_sha256']) is not str
                or not re.fullmatch('[0-9a-f]{64}', recipe['base_render_sha256'])
                or not isinstance(recipe['format_edits'], list)):
            raise ValueError('status original-byte recipe differs')
        base = _status_render(tree, recipe['style'])
        if digest(base) != recipe['base_render_sha256']:
            raise ValueError('status base rendering digest differs')
        pieces, previous = [], 0
        for edit in recipe['format_edits']:
            if not isinstance(edit, list) or len(edit) != 3 or type(edit[2]) is not str:
                raise ValueError('status byte edit shape differs')
            start, end = _status_integer(edit[0]), _status_integer(edit[1])
            if not previous <= start <= end <= len(base):
                raise ValueError('status byte edits overlap or exceed their one base rendering')
            pieces.extend((base[previous:start], edit[2].encode('utf-8')))
            previous = end
        pieces.append(base[previous:])
        body = b''.join(pieces)
        actual_blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        if (actual_blob, digest(body), len(body)) != (blob, identity, size):
            raise ValueError('restored status original length or hashes differ')
        compact = {'indent': None, 'compact': True, 'ensure_ascii': False, 'trailing': ''}
        if _status_render(_status_json_loads(body), compact) != _status_render(tree, compact):
            raise ValueError('status formatting edits changed typed source content')
        return body
    except (KeyError, TypeError, UnicodeError, RecursionError) as exc:
        raise ValueError('invalid status original-byte reconstruction') from exc


def status_record_candidate(path):
    """A finite selector only; original coordinates and owners remain mandatory."""
    return (type(path) is str and '\\' not in path and '\0' not in path
            and path.startswith('research/t20-live-20261009/')
            and all(part not in ('', '.', '..', '.git') for part in path.split('/'))
            and digest(path.encode('utf-8')) in STATUS_RECORD_PATH_HASHES)


def status_record_provider(path):
    return status_record_candidate(path) and digest(path.encode('utf-8')) in STATUS_RECORD_PROVIDER_HASHES


STATUS_RECORD_OWNER_BASE = '0784acddd4770f1190f758f264ba52b2b110bd27'
STATUS_RECORD_OWNER_TREE = '38b18f38db2e38dabe1ec391c07c0b0f2b20d574'
STATUS_RECORD_OWNER_ORIGINAL = {
    'research/t20-live-20261009/INDEX.json': (
        '533205328be61d4ef00734ec5ab1726af056ce24',
        '578b2f63c3038627a68c1d4cd816ca9f9a3cd973ee35864a5c22e3860f2f7483', 15728),
    'research/t20-live-20261009/README.md': (
        '0d225b8cf2973d28c9ff2bcfd215e364bb18ca42',
        '543cc8ea246fdc3f1fb03e0b41bb539dde2f23a7eeaa2ddf9178826840b5f139', 10196),
}


def status_owner_edition(root, baseline_rows, baseline):
    """Bind the two discovery owners without changing their original census."""
    paths = sorted(STATUS_RECORD_OWNERS)
    if not set(paths).intersection(baseline_rows):
        return {}
    if (not isinstance(baseline, dict)
            or (baseline.get('commit'), baseline.get('tree'))
            != (STATUS_RECORD_OWNER_BASE, STATUS_RECORD_OWNER_TREE)):
        raise ValueError('status owner original baseline differs')
    for path in paths:
        blob, _, size = STATUS_RECORD_OWNER_ORIGINAL[path]
        row = baseline_rows.get(path, {})
        if (row.get('path'), row.get('kind'), row.get('mode'), row.get('git_oid'), row.get('bytes')) != (
                path, 'blob', '100644', blob, size):
            raise ValueError('status owner original census coordinate differs: ' + path)
    root = _binding_record_root(root)
    indexed = {path: _administrative_git(root, 'ls-files', '--stage', '-z', '--', path)
               for path in paths}
    states = {path: _binding_record_current_state(root, path) for path in paths}
    edition = next((candidate for candidate in (STATUS_RECORD_OWNER_ORIGINAL, STATUS_RECORD_OWNERS)
                    if all(indexed[path] == ('100644 ' + candidate[path][0] + ' 0\t' + path + '\0').encode()
                           for path in paths)), None)
    if edition is None:
        raise ValueError('status owners are not one complete indexed edition')
    commit = _administrative_git(root, 'cat-file', 'commit', STATUS_RECORD_OWNER_BASE)
    if (hashlib.sha1(b'commit ' + str(len(commit)).encode() + b'\0' + commit).hexdigest()
            != STATUS_RECORD_OWNER_BASE
            or not commit.startswith(('tree ' + STATUS_RECORD_OWNER_TREE + '\n').encode())):
        raise ValueError('status owner original native commit or tree differs')
    for path in paths:
        blob, identity, size = STATUS_RECORD_OWNER_ORIGINAL[path]
        expected = ('100644 blob ' + blob + '\t' + path + '\0').encode()
        if _administrative_git(root, 'ls-tree', '-z', STATUS_RECORD_OWNER_BASE, '--', path) != expected:
            raise ValueError('status owner original native path, type, mode or blob differs')
        original = _administrative_git(root, 'cat-file', 'blob', blob)
        actual_blob = hashlib.sha1(b'blob ' + str(len(original)).encode() + b'\0' + original).hexdigest()
        if (actual_blob, digest(original), len(original)) != (blob, identity, size):
            raise ValueError('status owner original native bytes differ')
        blob, identity, size = edition[path]
        body = _administrative_bound_bytes(root, path, blob)
        if (len(body), digest(body)) != (size, identity):
            raise ValueError('status current owner bytes differ from its indexed edition')
    for path in paths:
        if (_binding_record_current_state(root, path) != states[path]
                or _administrative_git(root, 'ls-files', '--stage', '-z', '--', path) != indexed[path]):
            raise ValueError('status owner pair changed across edition qualification')
    if edition is STATUS_RECORD_OWNER_ORIGINAL:
        return {}
    return {path: {'path': path, 'kind': 'blob', 'mode': '100644',
                   'git_oid': edition[path][0], 'bytes': edition[path][2]} for path in paths}


def _status_record_owner_bytes(root):
    """The semantic owners must be current, ordinary, indexed and exact."""
    root = _binding_record_root(root)
    bodies, states = {}, {}
    for path, (blob, identity, size) in STATUS_RECORD_OWNERS.items():
        expected = ('100644 ' + blob + ' 0\t' + path + '\0').encode()
        before = _administrative_git(root, 'ls-files', '--stage', '-z', '--', path)
        if before != expected:
            raise ValueError('status current owner is absent or staged differently')
        present_before = _binding_record_current_state(root, path)
        states[path] = (before, present_before)
        body = _administrative_bound_bytes(root, path, blob)
        if ((len(body), digest(body)) != (size, identity)
                or _administrative_git(root, 'ls-files', '--stage', '-z', '--', path) != before
                or _binding_record_current_state(root, path) != present_before):
            raise ValueError('status current owner changed')
        bodies[path] = body
    for path, (indexed, present) in states.items():
        if (_administrative_git(root, 'ls-files', '--stage', '-z', '--', path) != indexed
                or _binding_record_current_state(root, path) != present):
            raise ValueError('status owner set changed across qualification')
    return bodies[STATUS_RECORD_INDEX]


def _status_record_catalog(raw):
    document = _status_json_loads(raw)
    try:
        if document['schema'] != 'scientific-status-owner-v3':
            raise ValueError('status current owner schema differs')
        sources, values = document['sources'], document['values']
        if not isinstance(sources, dict) or not isinstance(values, dict):
            raise ValueError('status source or value catalogue differs')
        rows = {}
        for source_id, source in sources.items():
            if (not re.fullmatch(r'S[0-9]{4}', source_id) or not isinstance(source, dict)
                    or not isinstance(source['aliases'], list) or not source['aliases']):
                raise ValueError('status source alias shape differs')
            identity = _status_identity(source)
            for path in source['aliases']:
                if (type(path) is not str or '\\' in path or '\0' in path
                        or not path.startswith('research/t20-live-20261009/')
                        or any(part in ('', '.', '..', '.git') for part in path.split('/'))
                        or path in rows):
                    raise ValueError('duplicate or unsafe status source alias')
                rows[path] = (source_id, identity)
        vector = b''.join((path + '\0' + name + '\0' + blob + '\0' + sha256 + '\0'
                           + str(size) + '\n').encode('utf-8')
                          for path, (name, (blob, sha256, size)) in sorted(rows.items()))
        selected = {path: row for path, row in rows.items() if status_record_candidate(path)}
        if (len(sources) != STATUS_RECORD_SOURCE_COUNT or len(rows) != STATUS_RECORD_ALIAS_COUNT
                or len(selected) != len(STATUS_RECORD_PATH_HASHES)
                or digest(vector) != STATUS_RECORD_CLASS_SHA256):
            raise ValueError('status original finite source class differs')
        return document, selected
    except (KeyError, TypeError, UnicodeError) as exc:
        raise ValueError('invalid status current owner catalogue') from exc


def _status_record_original_base(root):
    body = _administrative_git(root, 'cat-file', 'commit', STATUS_RECORD_BASE)
    if (hashlib.sha1(b'commit ' + str(len(body)).encode() + b'\0' + body).hexdigest()
            != STATUS_RECORD_BASE or not body.startswith(('tree ' + STATUS_RECORD_TREE + '\n').encode())):
        raise ValueError('status original native commit or tree differs')


def _status_record_bound_bytes(root, path, row, document, present):
    if _binding_record_present(root, path) != present:
        raise ValueError('status original presence changed before its read')
    source_id, (blob, identity, size) = row
    expected = ('100644 blob ' + blob + '\t' + path + '\0').encode()
    if _administrative_git(root, 'ls-tree', '-z', STATUS_RECORD_BASE, '--', path) != expected:
        raise ValueError('status original native path, blob or mode differs')
    expected_index = ('100644 ' + blob + ' 0\t' + path + '\0').encode()
    indexed = _administrative_git(root, 'ls-files', '--stage', '-z', '--', path)
    if indexed not in (b'', expected_index):
        raise ValueError('status original staged identity differs')
    original = _administrative_bound_bytes(root, path, blob)
    restored = _status_decode_body(document['sources'][source_id], document['values'])
    if ((len(original), digest(original)) != (size, identity) or restored != original):
        raise ValueError('status native original and restored owner bytes differ')
    if (_administrative_git(root, 'ls-files', '--stage', '-z', '--', path) != indexed
            or _binding_record_present(root, path) != present):
        raise ValueError('status source presence or index changed during its read')
    return restored


def status_record_bytes(root, path, identity=None, size=None):
    """Read an exact historical status source; ACTIVE remains preserved data."""
    if not status_record_candidate(path):
        raise ValueError('unqualified status source path')
    root = _binding_record_root(root)
    indexed = _administrative_git(root, 'ls-files', '--stage', '-z', '--', path)
    raw = _status_record_owner_bytes(root)
    document, catalog = _status_record_catalog(raw)
    if path not in catalog:
        raise ValueError('unqualified status original coordinate')
    expected_index = ('100644 ' + catalog[path][1][0] + ' 0\t' + path + '\0').encode()
    if indexed not in (b'', expected_index):
        raise ValueError('status original initial staged identity differs')
    present = _binding_record_present(root, path)
    present_state = _binding_record_current_state(root, path) if present else None
    if not present:
        _binding_record_role_context(root)
    _status_record_original_base(root)
    body = _status_record_bound_bytes(root, path, catalog[path], document, present)
    if ((identity is not None and (type(identity) is not str or digest(body) != identity))
            or (size is not None and (type(size) is not int or len(body) != size))):
        raise ValueError('status requested source identity differs')
    if _status_record_owner_bytes(root) != raw:
        raise ValueError('status current owner changed across the source read')
    if not present:
        _binding_record_role_context(root)
    if (_binding_record_present(root, path) != present
            or (present and _binding_record_current_state(root, path) != present_state)):
        raise ValueError('status current source changed across owner qualification')
    if _administrative_git(root, 'ls-files', '--stage', '-z', '--', path) != indexed:
        raise ValueError('status original index changed across owner qualification')
    return body


def status_record_absences(root, paths):
    """Qualify only requested actual absences under unchanged current roles."""
    requested = set(paths)
    if not requested or any(not status_record_candidate(path) for path in requested):
        raise ValueError('unqualified status absence selection')
    root = _binding_record_root(root)
    indexes = {path: _administrative_git(root, 'ls-files', '--stage', '-z', '--', path)
               for path in sorted(requested)}
    raw = _status_record_owner_bytes(root)
    document, catalog = _status_record_catalog(raw)
    if not requested <= set(catalog):
        raise ValueError('unqualified status original absence coordinate')
    for path, indexed in indexes.items():
        expected = ('100644 ' + catalog[path][1][0] + ' 0\t' + path + '\0').encode()
        if indexed not in (b'', expected):
            raise ValueError('status original initial staged identity differs')
    if any(_binding_record_present(root, path) for path in requested):
        raise ValueError('status absence qualifier received a present source')
    _binding_record_role_context(root)
    _status_record_original_base(root)
    for path in sorted(requested):
        _status_record_bound_bytes(root, path, catalog[path], document, False)
    if _status_record_owner_bytes(root) != raw:
        raise ValueError('status current owner changed across absence qualification')
    _binding_record_role_context(root)
    if any(_binding_record_present(root, path) for path in requested):
        raise ValueError('status owner or actual absence set changed')
    if any(_administrative_git(root, 'ls-files', '--stage', '-z', '--', path) != indexed
           for path, indexed in indexes.items()):
        raise ValueError('status original index changed across absence qualification')
    return requested


# Finite original checksum records; generated live manifests are excluded.
DIGEST_RECORD_BASE = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
DIGEST_RECORD_TREE_SHA256 = '8516d7f42ce675996fcc368efb2e1f66ec85c294d815e39855f3b2b4a5da68e0'
DIGEST_RECORD_GROUPS = {'docs/project-closure/ar8r-v11/post-merge-proposals/codex-corpus-synthesis-v14': ['SOURCE_SHA256SUMS'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/codex-corpus-synthesis-v14/audit': ['CANDIDATE_FREEZE_SHA256SUMS'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/external-challenges/challenger-a-common-intervention': ['SOURCE_SHA256SUMS'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/external-challenges/challenger-b-formal-ancestry': ['SOURCE_SHA256SUMS'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/external-challenges/challenger-b-formal-ancestry/source-files': ['MANIFEST.sha256',
                                                                                                                      'reviewed_source_sha256.txt'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-ap': ['SHA256SUMS'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES': ['PMR-007_DEEP_BA_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                                 'PMR-007_DEEP_BB_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                                 'PMR-007_DEEP_BC_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                                 'PMR-007_DEEP_BD_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                                 'PMR-007_DEEP_BE_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                                 'PMR-007_DEEP_BF_ADMISSION_HASHES.sha256',
                                                                                                 'PMR-007_DEEP_BG_ADMISSION_HASHES.sha256',
                                                                                                 'PMR-007_DEEP_BH_ADMISSION_HASHES.sha256',
                                                                                                 'PMR-007_DEEP_BI_ADMISSION_HASHES.sha256',
                                                                                                 'PMR-007_DEEP_BJ_ADMISSION_HASHES.sha256',
                                                                                                 'PMR-007_DEEP_BK_ADMISSION_HASHES.sha256',
                                                                                                 'PMR-007_DEEP_M_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                                 'PMR-007_DEEP_N_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                                 'PMR-007_DEEP_O_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                                 'PMR-007_DEEP_P_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                                 'PMR-007_DEEP_Q_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                                 'PMR-007_DEEP_R_ADMISSION_HASHES_SANITIZED.sha256'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE': ['PMR-007_DEEP_AA_V2_FROZEN_HASHES.sha256',
                                                                                                       'PMR-007_DEEP_BF_V1_FROZEN_HASHES.sha256',
                                                                                                       'PMR-007_DEEP_BG_V1_FROZEN_HASHES.sha256',
                                                                                                       'PMR-007_DEEP_BH_V1_FROZEN_HASHES.sha256',
                                                                                                       'PMR-007_DEEP_BI_V1_FROZEN_HASHES.sha256',
                                                                                                       'PMR-007_DEEP_BJ_V1_FROZEN_HASHES.sha256',
                                                                                                       'PMR-007_DEEP_BK_V1_FROZEN_HASHES.sha256',
                                                                                                       'PMR-007_DEEP_H_ADMISSION_HASHES_V1_REJECTED_COUNT_MISMATCH.sha256',
                                                                                                       'PMR-007_DEEP_K_V1_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_L_V1_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_P_V1_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_Q_V1_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_R_V1_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_S_V1_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_T_V1_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_T_V2_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_T_V3_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_T_V4_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_U_V1_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_U_V2_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_V_V1_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_V_V2_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_W_V1_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_W_V2_FROZEN_HASHES_SANITIZED.sha256',
                                                                                                       'PMR-007_DEEP_W_V3_FROZEN_HASHES_SANITIZED.sha256'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk': ['SHA256SUMS'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/VALIDATION_RECEIPTS': ['PMR-007_DEEP_AA_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AA_V3_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AB_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AB_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AC_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AC_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AD_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AD_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AE_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AE_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AF_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AF_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AG_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AG_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AH_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AH_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AI_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AI_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AJ_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AJ_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AK_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AK_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AL_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AL_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AM_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AM_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AN_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AN_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AO_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AO_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AP_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AP_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AQ_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AQ_V1_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AQ_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AR_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AR_V1_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AR_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AS_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AS_V1_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AS_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AT_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AT_V1_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AT_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AU_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AU_V1_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AU_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AV_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AV_V1_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AV_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AW_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AW_V1_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AW_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AX_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AX_V1_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AX_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AY_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AY_V1_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AY_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AZ_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AZ_V1_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_AZ_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_A_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_BF_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_BG_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_BH_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_BI_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_BJ_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_BK_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_DEEP_B_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_C_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_D_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_E_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_F_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_G_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_H_ADMISSION_HASHES_V2.sha256',
                                                                                             'PMR-007_DEEP_I_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                             'PMR-007_DEEP_J_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                             'PMR-007_DEEP_K_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                             'PMR-007_DEEP_L_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_DEEP_S_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                             'PMR-007_DEEP_T_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                             'PMR-007_DEEP_U_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                             'PMR-007_DEEP_V_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                             'PMR-007_DEEP_W_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND11_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND12_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND13_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND14_V1_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND14_V2_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND14_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND15_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND15_V1_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND15_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND16_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND16_V1_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND16_V2_FROZEN_HASHES.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND18_V1_FROZEN_HASHES_SANITIZED.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND18_V3_FROZEN_HASHES_SANITIZED.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND18_V4_ADMISSION_HASHES_SANITIZED.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND19_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND20_ADMISSION_HASHES.sha256',
                                                                                             'PMR-007_FRONTIER_ROUND20_V2_FROZEN_HASHES.sha256'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-bl-bv-semantic-reissue': ['SOURCE_SHA256SUMS'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-bl-bv-semantic-reissue/source-files': ['AR8R_PMR007_CURRENT_CONTINUATION_AFTER_DEEP_BV.yaml.sha256',
                                                                                                        'AR8R_PMR007_DEEP_BL_BV_BOUNDARY_REPORT.md.sha256'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-bw-cj-semantic-reissue': ['SOURCE_SHA256SUMS'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-bw-cj-semantic-reissue/source-files': ['SHA256SUMS'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-rounds11-20/REJECTED_AND_BLOCKED_EVIDENCE': ['PMR-007_FRONTIER_ROUND20_V1_FROZEN_HASHES.sha256'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-rounds11-20': ['SHA256SUMS'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-rounds11-20/VALIDATION_RECEIPTS': ['PMR-007_FRONTIER_ROUND20_ADMISSION_HASHES.sha256',
                                                                                               'PMR-007_FRONTIER_ROUND20_V2_FROZEN_HASHES.sha256'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files': ['SHA256SUMS'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/specialist-a/source-files': ['SHA256SUMS'],
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/specialist-b/source-files': ['MANIFEST.sha256'],
 'experiments/orthemology-v5-successors/source-store/18f002a663dc517f2380cc9f776d7817d4e5bb0988ab4cf88c7b1191134a102c': ['SHA256SUMS'],
 'experiments/orthemology-v5-successors/source-store/4bd854bbfda323abb9aa99594130eb388bd5f70c34bb4a84c1a78db3a010691b': ['SHA256SUMS'],
 'experiments/orthemology-v5-successors/source-store/9ab3df6e096f8158f755ea31408786248d04547d0bd7c38785770d7e9964e41e': ['SHA256SUMS'],
 'experiments/orthemology-v5-successors/source-store/c39d66e66d470c11cea130594ddc90708424a7d6d4028f20d371889ab3743124': ['MANIFEST.sha256'],
 'experiments/orthemology-v5-successors/source-store/c52d567e74562f17214173bdbf61b078e369fa3241e20e897d1713d48c8cd56d': ['SHA256SUMS'],
 'experiments/orthemology-v5-successors/source-store/f281d34cfdf3731f8c91244625146828c72a60acd7eacab60b51915caba1e644': ['SOURCE_ONLY_v1.sha256'],
 'research/t20-v6-20261012/sources/5ddd6de378a77f800abf874535b0396a79c06514ce11b65f8b99268ee445cb5f': ['CURRENT_FREEZE_SOURCE_HASHES.txt'],
 'research/t20-v6-20261012/sources/696da008a6189fd88e004a56af683d65cf608a04cecdc6b3c3ef88b0a954301e': ['ORIGINAL_HASHES_AFTER.txt'],
 'research/t20-v6-20261012/sources/af1d4e4b0174f2e874ddba1fc867735636440239d135c79edb6d2b39ca368d36': ['INPUT_HASHES.txt'],
 'research/t20-v6-20261012/sources/ce94319878c97e22e69fe70b2cea9c13e2336407dc7d073e087b439ecc554e7c': ['recompiled-source-hashes.txt'],
 'research/t20-v6-20261012/sources/f9a086fc2356bce74109a1527f123e66efa438264f6a0433950cc0c84f6e4ccd': ['ORIGINAL_HASHES_BEFORE.txt']}
DIGEST_RECORD_PATHS = {directory + "/" + name
    for directory, members in DIGEST_RECORD_GROUPS.items() for name in members}
DIGEST_PUBLIC_ROWS = {'research/t20-v6-20261012/sources/5ddd6de378a77f800abf874535b0396a79c06514ce11b65f8b99268ee445cb5f/CURRENT_FREEZE_SOURCE_HASHES.txt': 'b34a97aa437effe28f4568259c7bedd8a8b8ac9bd0516deecece3206da35a9b3',
 'docs/project-closure/ar8r-v11/post-merge-proposals/external-challenges/challenger-b-formal-ancestry/source-files/reviewed_source_sha256.txt': '31d8ce211a3cfd633d60ebcaa64fdc5c8c533b15632c3aae7b44cdd38e8e5352',
 'research/t20-v6-20261012/sources/696da008a6189fd88e004a56af683d65cf608a04cecdc6b3c3ef88b0a954301e/ORIGINAL_HASHES_AFTER.txt': 'ddc5ea76873e2fb03c5302853843d53cd212ff2d4f69e4207e617666b71c98e0',
 'research/t20-v6-20261012/sources/af1d4e4b0174f2e874ddba1fc867735636440239d135c79edb6d2b39ca368d36/INPUT_HASHES.txt': 'b9b4b38f0a54400d86c650df80109ac639db776011864674fe40d0f322491a88',
 'research/t20-v6-20261012/sources/ce94319878c97e22e69fe70b2cea9c13e2336407dc7d073e087b439ecc554e7c/recompiled-source-hashes.txt': '4e65e419f61b0d05c4ee8f70c470814558aeec75879f3853b5b05f66ea2ea57b',
 'research/t20-v6-20261012/sources/f9a086fc2356bce74109a1527f123e66efa438264f6a0433950cc0c84f6e4ccd/ORIGINAL_HASHES_BEFORE.txt': '683a79f3d50ad7d9fb55025b6ab4c636111a47c1861969feabc99f6367bbe48b'}
DIGEST_SUCCESSOR_ROWS = {'experiments/orthemology-v5-successors/source-store/c39d66e66d470c11cea130594ddc90708424a7d6d4028f20d371889ab3743124/MANIFEST.sha256': 'a340a77c84dc2cfa29144e883b40e756b346a0a720befce5567e48329d8c8b07',
 'experiments/orthemology-v5-successors/source-store/9ab3df6e096f8158f755ea31408786248d04547d0bd7c38785770d7e9964e41e/SHA256SUMS': 'e4e2b22ee6ffc2bad8298f5ff4e2faf50f63ae4bf1db428dcdc6ae55356de862',
 'experiments/orthemology-v5-successors/source-store/18f002a663dc517f2380cc9f776d7817d4e5bb0988ab4cf88c7b1191134a102c/SHA256SUMS': 'a1233e0d8e9a217934ed513841a922607916067e32f3ab9d0705ba64bac2cd93',
 'experiments/orthemology-v5-successors/source-store/f281d34cfdf3731f8c91244625146828c72a60acd7eacab60b51915caba1e644/SOURCE_ONLY_v1.sha256': '8fc718ca06b615fd9b7bfeb2ebe07b148197723e4eb3c0e14b331ed5560340e2',
 'experiments/orthemology-v5-successors/source-store/4bd854bbfda323abb9aa99594130eb388bd5f70c34bb4a84c1a78db3a010691b/SHA256SUMS': '4c87f6f6df1825f20fb97732cc9f3053ee834b156255603fc532bad126050fd1',
 'experiments/orthemology-v5-successors/source-store/c52d567e74562f17214173bdbf61b078e369fa3241e20e897d1713d48c8cd56d/SHA256SUMS': '7ff43a52d9d233833863ffd2d51d706341e98595954230bb490062dceb0875e7'}


def _digest_record_root(root):
    """Retain the supplied ordinary ancestry; never resolve an alias away."""
    root = pathlib.Path(root)
    if '..' in root.parts or '\\' in str(root):
        raise ValueError('historical digest repository uses a lexical alias')
    return _binding_record_root(root)


def _digest_record_state(root, path):
    root = _digest_record_root(root)
    if not _binding_record_present(root, path):
        return None
    return _binding_record_current_state(root, path)


def _digest_record_current_bytes(root, path, expected):
    """Reject a replacement descriptor before reading its body."""
    if expected is None or _digest_record_state(root, path) != expected:
        raise ValueError('historical digest current node changed before reading')
    target = pathlib.Path(root) / path
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | getattr(os, 'O_NOATIME', 0)
    state = lambda entry: (entry.st_dev, entry.st_ino, entry.st_mode, entry.st_size,
                           entry.st_mtime_ns, entry.st_ctime_ns)
    with os.fdopen(os.open(target, flags), 'rb') as stream:
        before = os.fstat(stream.fileno())
        if (not stat.S_ISREG(before.st_mode) or before.st_mode & 0o111
                or state(before) != expected):
            raise ValueError('historical digest current descriptor changed before reading')
        body = stream.read(before.st_size + 1)
        after = os.fstat(stream.fileno())
    if (state(after) != expected or _digest_record_state(root, path) != expected
            or len(body) != before.st_size):
        raise ValueError('historical digest current node changed during reading')
    return body


def _digest_record_bound_bytes(root, path, blob, initial):
    """Keep initial absence/presence, inode and staged identity through the read."""
    if _digest_record_state(root, path) != initial:
        raise ValueError('historical digest presence or node changed before reading')
    staged = _administrative_git(root, 'ls-files', '--stage', '-z', '--', path)
    expected = ('100644 ' + blob + ' 0\t' + path + '\0').encode()
    if staged not in (b'', expected):
        raise ValueError('historical digest staged identity differs')
    if _digest_record_state(root, path) != initial:
        raise ValueError('historical digest presence or node changed before native body read')
    original = _administrative_git(root, 'cat-file', 'blob', blob)
    if hashlib.sha1(b'blob ' + str(len(original)).encode() + b'\0' + original).hexdigest() != blob:
        raise ValueError('historical digest Git body differs')
    if _digest_record_state(root, path) != initial:
        raise ValueError('historical digest presence or node changed during native body read')
    if initial is not None and _digest_record_current_bytes(root, path, initial) != original:
        raise ValueError('historical digest present bytes differ')
    if _administrative_git(root, 'ls-files', '--stage', '-z', '--', path) != staged:
        raise ValueError('historical digest index changed during reading')
    if _digest_record_state(root, path) != initial:
        raise ValueError('historical digest presence or node changed after reading')
    return original


def _digest_record_read(root, path, initial, identity=None, size=None):
    body = _digest_record_bound_bytes(root, path, _digest_record_catalog(root)[path], initial)
    if ((identity is not None and digest(body) != identity)
            or (size is not None and len(body) != size)):
        raise ValueError('historical digest requested identity differs')
    return body


def _digest_record_catalog(root):
    """Authenticate the complete finite original checksum-record population."""
    root = _digest_record_root(root)
    commit = _administrative_git(root, 'cat-file', 'commit', DIGEST_RECORD_BASE)
    if hashlib.sha1(b'commit ' + str(len(commit)).encode() + b'\0' + commit).hexdigest() != DIGEST_RECORD_BASE:
        raise ValueError('historical digest revision differs')
    raw = _administrative_git(root, 'ls-tree', '-rz', '--full-tree', DIGEST_RECORD_BASE,
                              '--', *sorted(DIGEST_RECORD_PATHS))
    if len(DIGEST_RECORD_PATHS) != 176 or digest(raw) != DIGEST_RECORD_TREE_SHA256:
        raise ValueError('historical digest native population differs')
    bindings = {}
    for entry in raw.split(b'\0'):
        if not entry:
            continue
        metadata, name = entry.split(b'\t', 1)
        mode, kind, blob = metadata.decode('ascii').split()
        path = name.decode('utf-8')
        if (mode != '100644' or kind != 'blob' or path not in DIGEST_RECORD_PATHS
                or path in bindings or not re.fullmatch(r'[0-9a-f]{40}', blob)):
            raise ValueError('historical digest coordinate differs')
        bindings[path] = blob
    if set(bindings) != DIGEST_RECORD_PATHS:
        raise ValueError('historical digest class is incomplete')
    return bindings


def digest_record_bytes(root, path, identity=None, size=None):
    """Read an exact original record; preserve unknowns and never replay targets.

    Capture the current node before any native work. An initially absent alias
    cannot appear, nor a present node disappear or be replaced, during fallback.
    """
    if not isinstance(path, str) or path not in DIGEST_RECORD_PATHS:
        raise ValueError('unqualified historical digest path')
    root = _digest_record_root(root)
    initial = _digest_record_state(root, path)
    return _digest_record_read(root, path, initial, identity, size)


def digest_record_absences(root):
    """Authenticate the fixed original population and the same actual absence set."""
    root = _digest_record_root(root)
    initial = {path: _digest_record_state(root, path) for path in sorted(DIGEST_RECORD_PATHS)}
    for path, blob in _digest_record_catalog(root).items():
        _digest_record_bound_bytes(root, path, blob, initial[path])
    if any(_digest_record_state(root, path) != state for path, state in initial.items()):
        raise ValueError('historical digest actual absence set or current node changed')
    return {path for path, state in initial.items() if state is None}


def _digest_record_row_bytes(root, row, field, contracts):
    if not isinstance(row, dict) or not isinstance(row.get(field), str):
        raise ValueError('historical digest row is not a complete bound object')
    path = row[field]
    encoded = json.dumps(row, sort_keys=True, separators=(',', ':'),
                         ensure_ascii=False, allow_nan=False).encode('utf-8')
    if path not in contracts or digest(encoded) != contracts[path]:
        raise ValueError('historical digest complete row identity or role differs')
    return digest_record_bytes(root, path, row['public_sha256'], row['public_bytes'])


def digest_record_public_bytes(root, row):
    """Preserve all fields of the six existing public rows; admit no other row."""
    return _digest_record_row_bytes(root, row, 'repository_path', DIGEST_PUBLIC_ROWS)


def digest_record_successor_bytes(root, row):
    """Preserve six source IDs, archive/member coordinates and complete roles."""
    return _digest_record_row_bytes(root, row, 'public_path', DIGEST_SUCCESSOR_ROWS)


def _digest_record_view_binding(path):
    target = pathlib.Path(path).absolute()
    for name in DIGEST_RECORD_PATHS:
        parts = pathlib.PurePosixPath(name).parts
        if len(target.parts) > len(parts) and target.parts[-len(parts):] == parts:
            return target.parents[len(parts) - 1], name
    return None


def digest_record_view_bytes(path):
    """Physical custody view with witnessed, finite historical fallback only."""
    binding = _digest_record_view_binding(path)
    if binding is None:
        return pathlib.Path(path).read_bytes()
    root, name = binding
    initial = _digest_record_state(root, name)
    if initial is not None:
        return _digest_record_current_bytes(root, name, initial)
    try:
        return _digest_record_read(root, name, initial)
    except (ValueError, OSError) as error:
        raise OSError('historical digest is unavailable: ' + name) from error


def digest_record_view_text(path, encoding='utf-8', errors='strict'):
    return digest_record_view_bytes(path).decode(encoding, errors)


def digest_record_view_is_file(path):
    binding = _digest_record_view_binding(path)
    if binding is None:
        return pathlib.Path(path).is_file()
    try:
        digest_record_view_bytes(path)
    except (ValueError, OSError):
        return False
    return True


def digest_record_view_paths(root, directory):
    """Retain every observed entry and authenticate missing finite members."""
    root = _digest_record_root(pathlib.Path(root).absolute())
    directory = pathlib.Path(directory).absolute()
    if '..' in directory.parts:
        raise ValueError('historical digest custody directory uses a lexical alias')
    relative = directory.relative_to(root).as_posix().rstrip('/') + '/'
    observed = list(directory.rglob('*'))
    for name in sorted(DIGEST_RECORD_PATHS):
        if not name.startswith(relative):
            continue
        initial = _digest_record_state(root, name)
        if initial is not None:
            continue
        try:
            _digest_record_read(root, name, initial)
        except (ValueError, OSError):
            if _digest_record_state(root, name) != initial:
                raise ValueError('historical digest custody node changed during enumeration')
            continue  # Existing namespace/manifest checks still see unavailable members missing.
        observed.append(root / name)
    return observed


def _continuation_git(root, *args):
    result = subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs', *args],
                            cwd=root, capture_output=True, check=False)
    if result.returncode:
        raise ValueError('continuation copy Git identity unavailable')
    return result.stdout


def _continuation_object(root, kind, identity):
    body = _continuation_git(root, 'cat-file', kind, identity)
    header = kind.encode() + b' ' + str(len(body)).encode() + b'\0'
    if hashlib.sha1(header + body).hexdigest() != identity:
        raise ValueError('continuation copy Git object bytes differ')
    return body


def _continuation_copy_catalog(root):
    root = pathlib.Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('continuation copy requires an ordinary repository root')
    documents = {}
    for path, expected in CONTINUATION_COPY_METADATA.items():
        body = _regular_current_bytes(root, path)
        if (len(body), digest(body)) != expected:
            raise ValueError('continuation copy frozen metadata differs')
        documents[path] = json.loads(body)
    legacy = documents['docs/provenance/v5-research-continuations/SOURCE_MAP.json']['sources']
    successor = documents['docs/provenance/v5-successors/SOURCE_MAP.json']['sources']
    preservation = documents['docs/provenance/v5-successors/PRESERVATION.json']
    if preservation['base_commit'] != CONTINUATION_LEGACY_BASE:
        raise ValueError('continuation copy original version differs')
    preserved = {row['path']: row for row in preservation['files']}
    originals, retained = collections.defaultdict(list), collections.defaultdict(dict)
    for row in legacy:
        public_path = row.get('path')
        # Public provider names may change; original custody is inventory-owned.
        path = CONTINUATION_COPY_ROOT + str(row.get('original_sha256', '')) + '.lean'
        if isinstance(public_path, str) and public_path and path in preserved:
            originals[path].append(row)
    for row in successor:
        path = row.get('public_path') or ''
        if re.fullmatch(re.escape(CONTINUATION_RETAINED_ROOT) + r'[0-9a-f]{64}/[^/]+\.lean', path):
            identity = path[len(CONTINUATION_RETAINED_ROOT):].split('/')[0]
            if (row.get('projection') == 'EXACT' and row.get('derivation') is None
                    and row.get('original_sha256') == row.get('public_sha256') == identity
                    and row.get('original_bytes') == row.get('public_bytes')):
                retained[identity][path] = row
    result = {}
    for path, records in originals.items():
        identity = path[len(CONTINUATION_COPY_ROOT):-5]
        copies = retained.get(identity, {})
        if len(copies) != 1:
            continue
        canonical, copy = next(iter(copies.items()))
        size = copy['public_bytes']
        if any(row.get('projection') != 'EXACT' or row.get('derivation') is not None
               or row.get('original_sha256') != identity or row.get('sha256') != identity
               or row.get('original_bytes') != size or row.get('bytes') != size for row in records):
            raise ValueError('continuation copy source-ID identity differs')
        inventory = preserved.get(path, {})
        blob = inventory.get('git_blob_sha1')
        if ((inventory.get('bytes'), inventory.get('sha256')) != (size, identity)
                or not re.fullmatch('[0-9a-f]{40}', blob or '')):
            raise ValueError('continuation copy original inventory differs')
        result[path] = {'canonical': canonical, 'sha256': identity, 'bytes': size,
                        'blob': blob, 'sources': records, 'legacy_tree': preservation['base_tree']}
    excluded = CONTINUATION_COPY_ROOT + CONTINUATION_COPY_EXCLUDED + '.lean'
    if len(result) != CONTINUATION_COPY_COUNT + 1 or excluded not in result:
        raise ValueError('continuation copy finite class differs')
    del result[excluded]
    return result


def _continuation_bound_bytes(root, path, binding, *, current=None):
    root = pathlib.Path(root)
    canonical, blob = binding['canonical'], binding['blob']
    current = canonical if current is None else current
    for revision, names in ((CONTINUATION_LEGACY_BASE, (path,)),
                            (CONTINUATION_COPY_BASE, (path, canonical))):
        commit = _continuation_object(root, 'commit', revision)
        if revision == CONTINUATION_LEGACY_BASE and not commit.startswith(
                ('tree ' + binding['legacy_tree'] + '\n').encode()):
            raise ValueError('continuation copy original tree differs')
        expected = {('100644 blob ' + blob + '\t' + name).encode() for name in names}
        actual = set(_continuation_git(root, 'ls-tree', '-z', revision, '--', *names).split(b'\0')) - {b''}
        if actual != expected:
            raise ValueError('continuation copy original or retained mode/blob differs')
    original = _continuation_object(root, 'blob', blob)
    body = _regular_current_bytes(root, current)
    if (len(body), digest(body)) != (binding['bytes'], binding['sha256']) or original != body:
        raise ValueError('continuation retained copy or original Git bytes differ')
    indexed = collections.defaultdict(list)
    names = tuple(dict.fromkeys((path, canonical, current)))
    for raw in _continuation_git(root, 'ls-files', '--stage', '-z', '--', *names).split(b'\0'):
        if raw:
            metadata, name = raw.split(b'\t', 1)
            indexed[name.decode()].append(metadata.decode())
    expected = ['100644 ' + blob + ' 0']
    if (indexed[path] not in ([], expected)
            or indexed[canonical] not in ([], expected) or indexed[current] != expected):
        raise ValueError('continuation copy staged identity differs')
    for original_path in dict.fromkeys((path, canonical) if current != canonical else (path,)):
        target = root
        for part in original_path.split('/'):
            target = target / part
            if target.is_symlink():
                raise ValueError('continuation original path contains a symlink')
        if os.path.lexists(target) and _regular_current_bytes(root, original_path) != body:
            raise ValueError('present continuation original differs')
    return body


def continuation_copy_bytes(root, path, identity=None, size=None, source=None):
    """Authenticate an exact current copy; never recover arbitrary missing files."""
    if not re.fullmatch(re.escape(CONTINUATION_COPY_ROOT) + r'[0-9a-f]{64}\.lean', path):
        raise ValueError('unqualified continuation copy path')
    binding = _continuation_copy_catalog(root).get(path)
    if (binding is None or (identity is not None and identity != binding['sha256'])
            or (size is not None and size != binding['bytes'])
            or (source is not None and source not in binding['sources'])):
        raise ValueError('unqualified continuation copy or source-ID binding')
    return _continuation_formal_bound_bytes(root, path, binding)


def continuation_duplicate_paths(root):
    """Return only actual absences authenticated by the finite current-copy rule."""
    result = set()
    for path, binding in _continuation_copy_catalog(root).items():
        if not os.path.lexists(pathlib.Path(root) / path):
            _continuation_formal_bound_bytes(root, path, binding)
            result.add(path)
    return result


def _checkpoint_retarget_catalog(original):
    """Bind12 former providers to existing exact record routes without recursion."""
    encoded = json.dumps(CHECKPOINT_COPY_RETARGETS, separators=(',', ':')).encode()
    if (len(CHECKPOINT_COPY_RETARGETS) != 12
            or hashlib.sha256(encoded).hexdigest() != CHECKPOINT_COPY_RETARGETS_SHA256):
        raise ValueError('checkpoint retarget finite class differs')
    records = _checkpoint_record_members()
    result = {path: dict(binding) for path, binding in original.items()}
    seen, former = set(), set()
    for alias, prior, canonical, blob, identity, size in CHECKPOINT_COPY_RETARGETS:
        if (not all(isinstance(value, str) for value in (alias, prior, canonical, blob, identity))
                or alias in seen or prior in former or prior == canonical):
            raise ValueError('checkpoint retarget coordinates differ')
        binding = original.get(alias)
        expected = {'canonical': canonical, 'blob': blob, 'sha256': identity,
                    'bytes': size, 'mode': '100644'}
        if (binding is None or binding['canonical'] != prior
                or (binding['blob'], binding['sha256'], binding['bytes'], binding['mode'])
                    != (blob, identity, size, '100644')
                or records.get(prior) != expected):
            raise ValueError('checkpoint former provider or exact record binding differs')
        seen.add(alias)
        former.add(prior)
        result[alias].update(canonical=canonical, prior_canonical=prior)
    kept = {binding['canonical'] for binding in result.values()}
    if (len(seen) != 12 or len(former) != 12 or len(kept) != 73
            or kept & (set(result) | set(records))):
        raise ValueError('checkpoint retarget retained population differs')
    return result


def _checkpoint_copy_catalog():
    """The exact public snapshot class; no path discovery or basename fallback."""
    encoded = json.dumps(CHECKPOINT_COPY_MEMBERS, separators=(',', ':')).encode()
    if (len(CHECKPOINT_COPY_MEMBERS) != 87
            or hashlib.sha256(encoded).hexdigest() != CHECKPOINT_COPY_CATALOG_SHA256):
        raise ValueError('checkpoint copy finite class differs')
    result = {}
    for checkpoint, retained, member, blob, identity, size in CHECKPOINT_COPY_MEMBERS:
        if (not re.fullmatch(r'CP[0-9]{2}', checkpoint)
                or not re.fullmatch(r'CP[0-9]{2}', retained)
                or not isinstance(member, str) or '\\' in member or '\0' in member
                or any(p in ('', '.', '..', '.git') for p in member.split('/'))
                or not member.endswith(('.md', '.json'))
                or not re.fullmatch(r'[0-9a-f]{40}', blob)
                or not re.fullmatch(r'[0-9a-f]{64}', identity)
                or not isinstance(size, int) or isinstance(size, bool) or size <= 0):
            raise ValueError('checkpoint copy member identity differs')
        alias = CHECKPOINT_COPY_ROOT + checkpoint + '/' + member
        canonical = CHECKPOINT_COPY_ROOT + retained + '/' + member
        if alias in result:
            raise ValueError('duplicate checkpoint alias')
        result[alias] = {'canonical': canonical, 'blob': blob, 'sha256': identity,
                         'bytes': size, 'mode': '100644',
                         'original_checkpoint': checkpoint}
    kept = {row['canonical'] for row in result.values()}
    if len(result) != 87 or len(kept) != 85 or set(result) & kept:
        raise ValueError('checkpoint copy retained population differs')
    return _checkpoint_retarget_catalog(result)


def _checkpoint_bound_bytes(root, path, binding, *, current=None):
    """Authenticate one original coordinate and its exact retained public body."""
    root = pathlib.Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('checkpoint copy requires an ordinary repository root')
    canonical, blob = binding['canonical'], binding['blob']
    current = canonical if current is None else current
    try:
        # These unchanged Git primitives already authenticate exact object bytes.
        # Only two explicitly catalogued public paths and their known blob are read.
        _continuation_object(root, 'commit', CHECKPOINT_COPY_BASE)
        expected = {('100644 blob ' + blob + '\t' + name).encode()
                    for name in (path, canonical)}
        actual = set(_continuation_git(root, 'ls-tree', '-z', CHECKPOINT_COPY_BASE,
                                      '--', path, canonical).split(b'\0')) - {b''}
        if actual != expected:
            raise ValueError('checkpoint original or retained mode/blob differs')
        original = _continuation_object(root, 'blob', blob)
        owner_provider = (current == canonical and status_record_provider(canonical)
                          and not _binding_record_present(root, canonical))
        body = (status_record_bytes(root, canonical, binding['sha256'], binding['bytes'])
                if owner_provider else _regular_current_bytes(root, current))
        if (len(body), digest(body)) != (binding['bytes'], binding['sha256']) or body != original:
            raise ValueError('checkpoint retained body or original Git bytes differ')
        indexed = collections.defaultdict(list)
        names = tuple(dict.fromkeys((path, canonical, current)))
        for raw in _continuation_git(root, 'ls-files', '--stage', '-z',
                                     '--', *names).split(b'\0'):
            if raw:
                metadata, name = raw.split(b'\t', 1)
                indexed[name.decode()].append(metadata.decode())
        expected_index = ['100644 ' + blob + ' 0']
        current_indexes = ([], expected_index) if owner_provider else (expected_index,)
        if (indexed[path] not in ([], expected_index)
                or indexed[canonical] not in ([], expected_index)
                or indexed[current] not in current_indexes):
            raise ValueError('checkpoint copy staged identity differs')
        for original_path in dict.fromkeys((path, canonical) if current != canonical else (path,)):
            target = root
            for part in original_path.split('/'):
                target = target / part
                if target.is_symlink():
                    raise ValueError('checkpoint original path contains a symlink')
            if os.path.lexists(target) and _regular_current_bytes(root, original_path) != body:
                raise ValueError('present checkpoint original differs')
        if owner_provider and _binding_record_present(root, canonical):
            raise ValueError('checkpoint historical provider owner or actual absence differs')
        return body
    except OSError as exc:
        raise ValueError('checkpoint copy public dependency is unavailable') from exc


def _checkpoint_copy_bound_bytes(root, path, binding):
    """Authenticate a retargeted original together with its former provider.

    A former provider may be absent or staged absent only under the same
    original-history, exact-current-body, ordinary-mode and index checks as
    any other finite alias. Its corruption cannot be hidden by a good endpoint.
    """
    prior = binding.get('prior_canonical')
    if prior is not None:
        _checkpoint_bound_bytes(root, prior, binding)
    return _checkpoint_bound_bytes(root, path, binding)


def checkpoint_copy_bytes(root, path, identity=None, size=None):
    """Read a finite exact copy at its original checkpoint coordinate.

    The caller keeps the requested historical path and its dated evidence role.
    This does not execute or qualify a historical wrapper or permit retirement.
    """
    if not isinstance(path, str) or path not in CHECKPOINT_COPY_PATHS:
        raise ValueError('unqualified checkpoint copy path')
    binding = _checkpoint_copy_catalog().get(path)
    if (binding is None or (identity is not None and identity != binding['sha256'])
            or (size is not None and size != binding['bytes'])):
        raise ValueError('checkpoint copy requested identity differs')
    return _checkpoint_copy_bound_bytes(root, path, binding)


def checkpoint_duplicate_paths(root):
    """Return actual absences only after authenticating the complete finite class."""
    result = set()
    for path, binding in _checkpoint_copy_catalog().items():
        _checkpoint_copy_bound_bytes(root, path, binding)
        if not os.path.lexists(pathlib.Path(root) / path):
            result.add(path)
    return result


def _checkpoint_record_members():
    """Validate exactly76 inert record bindings independently of provider roles."""
    encoded = json.dumps(CHECKPOINT_RECORD_COPY_MEMBERS, separators=(',', ':')).encode()
    if (len(CHECKPOINT_RECORD_COPY_MEMBERS) != 76
            or hashlib.sha256(encoded).hexdigest() != CHECKPOINT_RECORD_COPY_CATALOG_SHA256):
        raise ValueError('checkpoint record finite class differs')
    result = {}
    for alias, canonical, blob, identity, size in CHECKPOINT_RECORD_COPY_MEMBERS:
        for path in (alias, canonical):
            if (not isinstance(path, str) or not path.startswith('research/t20-live-20261009/')
                    or '\\' in path or '\0' in path or ':' in path
                    or any(p in ('', '.', '..', '.git') for p in path.split('/'))
                    or not path.endswith('.json')):
                raise ValueError('checkpoint record coordinate differs')
        if (not alias.startswith(CHECKPOINT_COPY_ROOT) or alias in result or alias == canonical
                or not re.fullmatch(r'[0-9a-f]{40}', blob)
                or not re.fullmatch(r'[0-9a-f]{64}', identity)
                or not isinstance(size, int) or isinstance(size, bool) or size <= 0):
            raise ValueError('checkpoint record identity differs')
        result[alias] = {'canonical': canonical, 'blob': blob, 'sha256': identity,
                         'bytes': size, 'mode': '100644'}
    kept = {row['canonical'] for row in result.values()}
    if len(result) != 76 or len(kept) != 65 or set(result) & kept:
        raise ValueError('checkpoint record retained population differs')
    return result


def _checkpoint_record_copy_catalog():
    """Keep original logical contexts and all surviving earlier-class providers."""
    result = _checkpoint_record_members()
    kept = {row['canonical'] for row in result.values()}
    earlier = _checkpoint_copy_catalog()
    earlier_kept = {row['canonical'] for row in earlier.values()}
    if set(result) & (set(earlier) | earlier_kept) or kept & set(earlier):
        raise ValueError('checkpoint record retained population differs')
    return result


def checkpoint_record_copy_bytes(root, path, identity=None, size=None):
    """Return exact recorded bytes while the caller retains its original path."""
    if not isinstance(path, str) or path not in CHECKPOINT_RECORD_COPY_PATHS:
        raise ValueError('unqualified checkpoint record path')
    binding = _checkpoint_record_copy_catalog().get(path)
    if (binding is None or (identity is not None and identity != binding['sha256'])
            or (size is not None and size != binding['bytes'])):
        raise ValueError('checkpoint record requested identity differs')
    return _checkpoint_bound_bytes(root, path, binding)


def checkpoint_record_duplicate_paths(root):
    """Authenticate the complete record class before admitting exact absences."""
    result = set()
    for path, binding in _checkpoint_record_copy_catalog().items():
        _checkpoint_bound_bytes(root, path, binding)
        if not os.path.lexists(pathlib.Path(root) / path):
            result.add(path)
    return result


def _checkpoint_code_members():
    """Validate52 exact archived code bindings and their34 existing public rows."""
    encoded = json.dumps(CHECKPOINT_CODE_COPY_MEMBERS, separators=(',', ':')).encode()
    public = json.dumps(CHECKPOINT_CODE_PUBLIC_MEMBERS, separators=(',', ':')).encode()
    if (len(CHECKPOINT_CODE_COPY_MEMBERS) != 52
            or hashlib.sha256(encoded).hexdigest() != CHECKPOINT_CODE_COPY_CATALOG_SHA256
            or len(CHECKPOINT_CODE_PUBLIC_MEMBERS) != 34
            or hashlib.sha256(public).hexdigest() != CHECKPOINT_CODE_PUBLIC_SHA256
            or CHECKPOINT_CODE_PUBLIC_PATHS != frozenset(CHECKPOINT_CODE_PUBLIC_MEMBERS)):
        raise ValueError('checkpoint code finite class differs')
    result = {}
    for alias, canonical, blob, identity, size in CHECKPOINT_CODE_COPY_MEMBERS:
        for path in (alias, canonical):
            if (not isinstance(path, str) or not path.startswith('research/t20-live-20261009/')
                    or '\\' in path or '\0' in path or ':' in path
                    or any(p in ('', '.', '..', '.git') for p in path.split('/'))
                    or not path.endswith('.py')):
                raise ValueError('checkpoint code coordinate differs')
        if (not alias.startswith(CHECKPOINT_COPY_ROOT) or alias in result or alias == canonical
                or not re.fullmatch(r'[0-9a-f]{40}', blob)
                or not re.fullmatch(r'[0-9a-f]{64}', identity)
                or not isinstance(size, int) or isinstance(size, bool) or size <= 0):
            raise ValueError('checkpoint code identity differs')
        result[alias] = {'canonical': canonical, 'blob': blob, 'sha256': identity,
                         'bytes': size, 'mode': '100644'}
    kept = {row['canonical'] for row in result.values()}
    if (len(result) != 52 or len(kept) != 43 or set(result) & kept
            or not CHECKPOINT_CODE_PUBLIC_PATHS < set(result)):
        raise ValueError('checkpoint code retained population differs')
    return result


def _checkpoint_package_retarget_catalog(original):
    """Keep all ten former providers authenticated at their original coordinates."""
    encoded = json.dumps(CHECKPOINT_PACKAGE_RETARGETS, separators=(',', ':')).encode()
    if (len(CHECKPOINT_PACKAGE_RETARGETS) != 10
            or hashlib.sha256(encoded).hexdigest() != CHECKPOINT_PACKAGE_RETARGETS_SHA256):
        raise ValueError('checkpoint package retarget finite class differs')
    code = _checkpoint_code_members()
    result = {path: dict(binding) for path, binding in original.items()}
    seen, former = set(), set()
    for alias, prior, canonical, blob, identity, size in CHECKPOINT_PACKAGE_RETARGETS:
        if (not all(isinstance(value, str) for value in (alias, prior, canonical, blob, identity))
                or alias in seen or prior in former or prior == canonical):
            raise ValueError('checkpoint package retarget coordinates differ')
        binding = original.get(alias)
        expected = {'canonical': canonical, 'blob': blob, 'sha256': identity,
                    'bytes': size, 'mode': '100644'}
        if (binding is None or binding['canonical'] != prior
                or (binding['blob'], binding['sha256'], binding['bytes'], binding['mode'])
                    != (blob, identity, size, '100644')
                or code.get(prior) != expected):
            raise ValueError('checkpoint package former provider binding differs')
        seen.add(alias)
        former.add(prior)
        result[alias].update(canonical=canonical, prior_canonical=prior)
    kept = {binding['canonical'] for binding in result.values()}
    if (len(seen) != 10 or len(former) != 10 or len(kept) != 16
            or kept & (set(result) | set(code))):
        raise ValueError('checkpoint package retarget retained population differs')
    return result


def _checkpoint_code_copy_catalog():
    """Preserve every prior class and all final providers without recursion."""
    result = _checkpoint_code_members()
    kept = {row['canonical'] for row in result.values()}
    earlier = {**_checkpoint_copy_catalog(), **_checkpoint_record_copy_catalog(),
               **_checkpoint_package_copy_catalog()}
    earlier_kept = {row['canonical'] for row in earlier.values()}
    if set(result) & (set(earlier) | earlier_kept) or kept & set(earlier):
        raise ValueError('checkpoint code retained population differs')
    return result


def checkpoint_code_copy_bytes(root, path, identity=None, size=None):
    """Return exact inert source bytes, preserving the requested logical context."""
    if not isinstance(path, str) or path not in CHECKPOINT_CODE_COPY_PATHS:
        raise ValueError('unqualified checkpoint code path')
    binding = _checkpoint_code_copy_catalog().get(path)
    if (binding is None or (identity is not None and identity != binding['sha256'])
            or (size is not None and size != binding['bytes'])):
        raise ValueError('checkpoint code requested identity differs')
    return _checkpoint_bound_bytes(root, path, binding)


def checkpoint_code_duplicate_paths(root):
    """Admit actual52 absences only after authenticating every exact source."""
    result = set()
    for path, binding in _checkpoint_code_copy_catalog().items():
        _checkpoint_bound_bytes(root, path, binding)
        if not os.path.lexists(pathlib.Path(root) / path):
            result.add(path)
    return result


def _checkpoint_package_copy_catalog():
    """Receive the exact26 additional members of five reviewed duplicate packages."""
    encoded = json.dumps(CHECKPOINT_PACKAGE_COPY_MEMBERS, separators=(',', ':')).encode()
    if (len(CHECKPOINT_PACKAGE_COPY_MEMBERS) != 26
            or hashlib.sha256(encoded).hexdigest() != CHECKPOINT_PACKAGE_COPY_CATALOG_SHA256):
        raise ValueError('checkpoint package finite class differs')
    result = {}
    for alias, canonical, blob, identity, size in CHECKPOINT_PACKAGE_COPY_MEMBERS:
        for path in (alias, canonical):
            if (not isinstance(path, str) or not path.startswith(CHECKPOINT_COPY_ROOT)
                    or '\\' in path or '\0' in path or ':' in path
                    or any(p in ('', '.', '..', '.git') for p in path.split('/'))
                    or not path.endswith(('.py', '.md', '.json'))):
                raise ValueError('checkpoint package coordinate differs')
        if (alias in result or alias == canonical
                or not re.fullmatch(r'[0-9a-f]{40}', blob)
                or not re.fullmatch(r'[0-9a-f]{64}', identity)
                or not isinstance(size, int) or isinstance(size, bool) or size <= 0):
            raise ValueError('checkpoint package identity differs')
        result[alias] = {'canonical': canonical, 'blob': blob, 'sha256': identity,
                         'bytes': size, 'mode': '100644'}
    kept = {row['canonical'] for row in result.values()}
    earlier = {**_checkpoint_copy_catalog(), **_checkpoint_record_copy_catalog()}
    earlier_kept = {row['canonical'] for row in earlier.values()}
    suffixes = collections.Counter(pathlib.PurePosixPath(path).suffix for path in result)
    if (len(result) != 26 or len(kept) != 26 or set(result) & kept
            or suffixes != {'.py': 21, '.md': 3, '.json': 2}
            or set(result) & (set(earlier) | earlier_kept) or kept & set(earlier)):
        raise ValueError('checkpoint package retained population differs')
    return _checkpoint_package_retarget_catalog(result)


def checkpoint_package_copy_bytes(root, path, identity=None, size=None):
    """Return inert source bytes at their requested original historical coordinate.

    No source is imported, compiled or executed, and no new public projection
    row is admitted by this byte route. Historical replay remains separate.
    """
    if not isinstance(path, str) or path not in CHECKPOINT_PACKAGE_COPY_PATHS:
        raise ValueError('unqualified checkpoint package path')
    binding = _checkpoint_package_copy_catalog().get(path)
    if (binding is None or (identity is not None and identity != binding['sha256'])
            or (size is not None and size != binding['bytes'])):
        raise ValueError('checkpoint package requested identity differs')
    return _checkpoint_copy_bound_bytes(root, path, binding)


def checkpoint_package_duplicate_paths(root):
    """Admit exact26 absences only after authenticating the whole package class."""
    result = set()
    for path, binding in _checkpoint_package_copy_catalog().items():
        _checkpoint_copy_bound_bytes(root, path, binding)
        if not os.path.lexists(pathlib.Path(root) / path):
            result.add(path)
    return result



# Original public source-lock/input documents consolidated in the existing
# successor registry. Historical status and source-ID rows remain unchanged;
# this current-owner route neither reads historical input bodies nor runs them.
SUCCESSOR_INPUT_REGISTRY = 'experiments/orthemology-v5-successors/registry.json'
SUCCESSOR_INPUT_REGISTRY_ORIGINAL = ('2eb0d0b7bcd2227e72aacc069d491ac2c0d8704e',
 'bd3a917d7225c18112915f5afaef373a864d176880bd6045c9ea291dd2308088',
 20278)
SUCCESSOR_INPUT_REGISTRY_COMPACT = ('779b9b2b1b606b639acbae817bcfe0b449db87cb',
 'abdf460e94482b8585507dbe02e4b2580c6a511cb30a1851c3fc2b21f96d95e6',
 247542)
# The live result/status owner makes the separate calculus map redundant.
# Only this exact registry edition may recover its original historical view.
SUCCESSOR_INPUT_REGISTRY_CALCULUS = ('b623182df73c1d821d7d132ae092c7e7edf7abd3', 'a053989dc9c6dce6de4ec4208f48be8b1b0a66c284600b3dd17992c46aca7af7', 247365)
SUCCESSOR_CALCULUS_MAP = 'docs/provenance/v5-successors/CALCULUS_MAP.json'
SUCCESSOR_CALCULUS_MAP_IDENTITY = ('c00b45d757ee35877bc748351a6185faa6a1c360', 'd0644ef40458d17ac19710e4d1ecdc2cc974a54d73b4053641979f9ce1f74759', 69376)
SUCCESSOR_CALCULUS_RESULTS = 'docs/provenance/v5-successors/RESULT_STATUS.json'
SUCCESSOR_CALCULUS_RESULT_IDENTITY = ('de45612a3d7d68b78ed65dacf4dc8a9080b00f9b', '3e5917699c40b50fbd22ee4120b365b70bc32123b27d6ff9dac8eee9b1c5192e', 855613)
SUCCESSOR_CALCULUS_GUIDES = {'docs/architecture/V5-RESEARCH-SUCCESSORS-07-15.md': {'current': ('a6026e3780b3a6025878891f94cab66354b97efe',
                                                                   'a55842d9e674e018c2916c155050d312f74cef96c1788fde34a20d88af5f75cc',
                                                                   12354),
                                                       'original': ('92c1dd8d70889fa1c68e4a062866a6152225cc68',
                                                                    'e39d4df2df63902276fe9279f9458e1ed12980c743a3c58be07827d7097453be',
                                                                    12349),
                                                       'original_text': 'The [calculus '
                                                                        'map](../provenance/v5-successors/CALCULUS_MAP.json) '
                                                                        'preserves the\n',
                                                       'replacement': 'The [result '
                                                                      'statements](../provenance/v5-successors/RESULT_STATUS.json) '
                                                                      'preserve the\n'},
 'docs/provenance/v5-successors/README.md': {'current': ('4f160445222eb75c4afdb2710f44982737668f0a',
                                                         '233561ef29c12585d4fcc76fa18591127f9f3bb001fcee7ad46a8a356f654537',
                                                         8213),
                                             'original': ('3a4a712c3c5b27a45d693444ccd0603c708e9d80',
                                                          '1a5e06b45752fc2d01118b39550fdea297d5781954111a589c81e612f0823c93',
                                                          8164),
                                             'original_text': '| [CALCULUS_MAP](CALCULUS_MAP.json) '
                                                              '| Separate public P01DF, current '
                                                              'Has, HasPlus, HasE and '
                                                              'operational-model owners |',
                                             'replacement': '| Calculus and operational model in '
                                                            '[RESULT_STATUS](RESULT_STATUS.json) | '
                                                            'Separate public P01DF, current Has, '
                                                            'HasPlus, HasE and operational-model '
                                                            'owners; no adoption |'}}

SUCCESSOR_INPUT_IDENTITIES = {'experiments/orthemology-v5-successors/source-store/0fa8d05ed79fae8494e902456594ba0ab5805d8cf653547c870d337f3db60227/ACCEPTED_INPUTS.json': ('9c6b8a36c8322a84bc60960354a798491f46a42e',
                                                                                                                                              '0fa8d05ed79fae8494e902456594ba0ab5805d8cf653547c870d337f3db60227',
                                                                                                                                              9661),
 'experiments/orthemology-v5-successors/source-store/28daa5deacd7358a75f1ccf7b2beededd4b323218dfd3c0dcde37c64415117e7/source-lock.json': ('f5f31b17a11692e540fecac986571d0810eae80b',
                                                                                                                                          '28daa5deacd7358a75f1ccf7b2beededd4b323218dfd3c0dcde37c64415117e7',
                                                                                                                                          11769),
 'experiments/orthemology-v5-successors/source-store/44677823653e8e914ca7e8e4f582c08d6834bbe57c2835e8b0e4ddbca157eac8/SOURCE_IDENTITIES.json': ('4ae7354b188ce45097d72b4ac8795ef38ab7444e',
                                                                                                                                                '44677823653e8e914ca7e8e4f582c08d6834bbe57c2835e8b0e4ddbca157eac8',
                                                                                                                                                10061),
 'experiments/orthemology-v5-successors/source-store/4c6d10a5d818dda9b5f68b8c8bdd6d9ec8a053e584e6aaa70e8c014cb49fbb14/DEPENDENCIES.json': ('e4ba2d129645b64d614f2f9d130f23ab577cb7de',
                                                                                                                                           '4c6d10a5d818dda9b5f68b8c8bdd6d9ec8a053e584e6aaa70e8c014cb49fbb14',
                                                                                                                                           911),
 'experiments/orthemology-v5-successors/source-store/54638026fd05b40e780d1ed5d51bbd286398926e074b487f746237b5dd816be0/source-lock.json': ('fc50ba0dc4d991fe073b877998579cb7c69fefcd',
                                                                                                                                          '54638026fd05b40e780d1ed5d51bbd286398926e074b487f746237b5dd816be0',
                                                                                                                                          27255),
 'experiments/orthemology-v5-successors/source-store/59f9f607436e2b70ba2b8060aafcbf5edbd80f5c5c69553fe43447d039589924/lake-manifest.json': ('0e5527b93cab98dc17ea2bae63c47a2e97d93d09',
                                                                                                                                            '59f9f607436e2b70ba2b8060aafcbf5edbd80f5c5c69553fe43447d039589924',
                                                                                                                                            3530),
 'experiments/orthemology-v5-successors/source-store/5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752/mathlib-lake-manifest.json': ('92a8049abc1f1b43ae2b4a6605616034f0dd2682',
                                                                                                                                                    '5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752',
                                                                                                                                                    2786),
 'experiments/orthemology-v5-successors/source-store/5ca88d5793fb2283badb16c8d722b777e0e9eb49198043b9335a198d572060c7/MODULES.json': ('fb6800f3c9a97318f042984fa44bc8b653ee86bf',
                                                                                                                                      '5ca88d5793fb2283badb16c8d722b777e0e9eb49198043b9335a198d572060c7',
                                                                                                                                      2143),
 'experiments/orthemology-v5-successors/source-store/72293db56804c56c017582d7d22f8dc21a985ab37ff258ac789160c2dfeb7c63/sense-source-lock.json': ('08686a52836bd38618c89714033f5773e0aa8b7b',
                                                                                                                                                '72293db56804c56c017582d7d22f8dc21a985ab37ff258ac789160c2dfeb7c63',
                                                                                                                                                3700),
 'experiments/orthemology-v5-successors/source-store/7dc06e97812b481caac84ca86cc685c2fb255fdc119f650b83cc6851dc085e61/preserved-module-lock.json': ('749a698d39a4b7331db8da32adadbfdce8ce0500',
                                                                                                                                                    '7dc06e97812b481caac84ca86cc685c2fb255fdc119f650b83cc6851dc085e61',
                                                                                                                                                    13881),
 'experiments/orthemology-v5-successors/source-store/8981fe18fb0d182dfbab01142f250354846dfb691c873d8d1ced71d3f1df3f4c/SOURCE_MANIFEST.json': ('a453c3cab30144a42a0fee620e79be164bd9004d',
                                                                                                                                              '8981fe18fb0d182dfbab01142f250354846dfb691c873d8d1ced71d3f1df3f4c',
                                                                                                                                              54364),
 'experiments/orthemology-v5-successors/source-store/95927e700cd403a2651b33280d052a8c972b12bca48c5cac26a1643c14a80cc6/VERIFICATION.json': ('dc4b5bf39147633e519ce26714fa6ac8d45c2b52',
                                                                                                                                           '95927e700cd403a2651b33280d052a8c972b12bca48c5cac26a1643c14a80cc6',
                                                                                                                                           10917),
 'experiments/orthemology-v5-successors/source-store/9eaffaa788991447cf64938183de0e982b467d333dd9a369f11c0c99a0be595c/DEPENDENCY_PINS.json': ('1b4b907f9a07e510966cc556394328332503e6ad',
                                                                                                                                              '9eaffaa788991447cf64938183de0e982b467d333dd9a369f11c0c99a0be595c',
                                                                                                                                              1411),
 'experiments/orthemology-v5-successors/source-store/a774b663b6f6c6dfe81f7b6272cc57b8059a5bbfc7428ca4d0c41e0ba0fd88f2/TOOLCHAIN_REQUIREMENTS.json': ('b4f789777f78dfeea7396030f43de19effaab911',
                                                                                                                                                     'a774b663b6f6c6dfe81f7b6272cc57b8059a5bbfc7428ca4d0c41e0ba0fd88f2',
                                                                                                                                                     1930),
 'experiments/orthemology-v5-successors/source-store/a919102c102ff3d07b447f52490266aca76afa4f84a972e2f3d78b3470f97a7a/INPUTS.json': ('8f24186f63a4bf8d8170f4966d81499e25cd325a',
                                                                                                                                     'a919102c102ff3d07b447f52490266aca76afa4f84a972e2f3d78b3470f97a7a',
                                                                                                                                     3067),
 'experiments/orthemology-v5-successors/source-store/b7500882ab904ebc84f3f28a036d687a54f5f023eac839b6177a1d65b679874f/INPUT_SOURCE_MANIFEST.json': ('6c1cd045289ee6c80141e467f1571ff56c8ad626',
                                                                                                                                                    'b7500882ab904ebc84f3f28a036d687a54f5f023eac839b6177a1d65b679874f',
                                                                                                                                                    13212),
 'experiments/orthemology-v5-successors/source-store/bd800ff0214d7a382feb5da185d706766185fa309794ab52b2ad9e26444f613c/source-lock.json': ('84aa71aab1aa6f093a903667e9ba43b2e3379c55',
                                                                                                                                          'bd800ff0214d7a382feb5da185d706766185fa309794ab52b2ad9e26444f613c',
                                                                                                                                          33103),
 'experiments/orthemology-v5-successors/source-store/f7bda53cf932963883223c7f14f305b1354b35207d2a50da3c0dfcc2e3813eec/SOURCE_LOCK.json': ('c9e307e8f56b5f422c7c37ce81b2ff9b1d6911ac',
                                                                                                                                          'f7bda53cf932963883223c7f14f305b1354b35207d2a50da3c0dfcc2e3813eec',
                                                                                                                                          1293),
 'experiments/orthemology-v5-successors/source-store/fc51e32962e76ac4c5ebef5c3154b5c4a1ab6061aeb018db712d128ee6dac210/CANDIDATE_v1.json': ('efb2c86d08dc320547b45f6235491d49d0ad3cbd',
                                                                                                                                           'fc51e32962e76ac4c5ebef5c3154b5c4a1ab6061aeb018db712d128ee6dac210',
                                                                                                                                           1436)}
SUCCESSOR_INPUT_PATHS = frozenset(SUCCESSOR_INPUT_IDENTITIES)
SUCCESSOR_INPUT_SOURCE_ROWS = {'D04-SRC-a85d94dc414a670c7a8f': 'ebbbbcba2ed7fcfc88d63f8ab81be953fe45005fd723b5f6a465565abe162642',
 'D04-SRC-be2c9366c9dcd528896a': '36a8ed1f1735a68428bc83e4414b83c91ec20e5bd7d768e1f4ddd6550bf3cec4',
 'D17-T14-OCCURRENCE-LOCK': '6a7289058f39dcacb5bf439a1247469499e7b5805f67f7b62f3f61b17ba215f0',
 'D17-T14-SENSE-LOCK': '181874ad231690d68a8e0da0f7cfe72730ec36de6a1e66e2e915c4b3914124de',
 'T10-SOURCE-MATHLIB-LOCK': 'b390b2fa34594df1c0a17f469c1b12ebfa12ea72a1afc540ec2c03f9dcf590d5',
 'T10-SOURCE-TOOLCHAIN': '95930f09e34928b638caad4673ec3a28d6ba619e405ee345625e18bfdfbb76f7',
 'T15-EMPIRICAL-INPUTS': '2622157726e160b4bc62699ae8a2ce093c08c76fc25f514f7486389dd6ca9b19',
 'T16-SRC-558248588a84c4008c9f': '9e79cef98c755b5e6b6f80d6fd5614be44e56cf18c3634881ab061145d065d8f',
 'T16-SRC-5e89ebdc28d2c56f623b': '074fc08e953e04f2ae15bfb8e35e71026a8ec5e97f58e0fafbb4d24c3546c03f',
 'T16-SRC-92f6c5b5ed52c8f0f5b9': '64340de02564e21c1b885c3fd757d56e4d24582af06858c855395081dc3dcac6',
 'T18-SRC-ad5b98addd9ac45e786f': 'f06ac028a52bc105ae02bc41143d6dc174c22f0becc3c21551824e9f2caf2b76',
 'T20-SRC-08ebd6db94fc7f4d3631': '915c7d67fe0eaaacaafc3de9a80561baf19c08ea7e7cf7d8b116bb5afac47595',
 'T20-SRC-0ac8c842fa418387529e': '7880577635d065e15049ea8f05956f292d42ee080d3e91a6b884d0b45259b9d9',
 'identity-src-1c4b694e76a97ff0a4f3': 'b0555ac411a150b116107c8d5ac7d4f91f2bd94cf7c27cc53e31d16807cf3bb3',
 'identity-src-3a568ae64ac6477c0a72': '4ed8c27b9f93eb8cbd8a791477ab30fa8f3185e3126b32b7f26f0075ef3c4a02',
 'identity-src-3ef69ec0388c759d402a': 'e2bb40c54691cef5f04ac4f437042fe33e10ba7478541c30026289ee8ffa9645',
 'identity-src-4d2242ca386abb9fb05c': '3b471428146cf211b10a8f27e4f42d9d9131b11695acdc741e4e48421c4a19c0',
 'identity-src-5c6cec97594b89d6e3f9': '367b552dff0d0ea3aa23e362115a27b00656d37ccdd5772a4d00e8ece74fc8d9',
 'identity-src-75a60db349c64e493278': 'fafd1a9f669c6d077986d5fce70941d0df732854955c6d7d69c59b2fa048ddae',
 'identity-src-812be4cd57020df2dda2': 'de7838a5ad15d3fa723d6133db466fa2412f700e26b9a6af5149d2199bf3265d',
 'identity-src-9e0f90d4821dac7a884e': '783b47c72569db73f5ce1739d1d565886b65df0ff8d8b0acececa1c87986a67a',
 'identity-src-cd9196f31acf59c1f322': 'fbed0e4f6d3fadf7871236fe1e73f6c666c9f243472f0e1f4bad1b020611d745',
 'identity-src-e57c31ee021169826e13': '5058bfc1fe8f686b95b11a557bc2b5699aa553e64c767a9603df56a72d5b5392',
 'identity-src-f76bd800c9ca61417210': '230cc95e46272e4dad737e5f08cbef79329ac25b02e58f1fc9ff566edabe814b',
 'identity-src-fc97dc05921345d7812e': '437ae474ecbbab0c32dfce5bfe3f7815648ee691f791a706a70efae19b02e8c9',
 's0715-62eea502abc73f088bab': '0a506bbf9ceadcba7d4ffef63435532bd7e0eac6db82de12d000d163e9c0590e',
 's0715-65f87c96b2f69867bfbd': 'f0ebd5df2c8baf5cf544b713809a723b29130d95066ff22ea3fad86f87279bec',
 's0715-8bc1d7ed6f374d6baed3': '043280dddea1c4ba88b541e3daf4cb1b860416d9fb7d4189736bc0c82ff4c156',
 's0715-bd1e3387b8323ac0da4c': '28d967d45608efd982d05ae0f3da6871729eeda1e4bc7b4bc486ead9ecc6c64c'}
SUCCESSOR_INPUT_ALLOWLIST_ROWS = {'experiments/orthemology-v5-successors/source-store/0fa8d05ed79fae8494e902456594ba0ab5805d8cf653547c870d337f3db60227/ACCEPTED_INPUTS.json': '2bcc7a99b1f59efd3b61795dc1e1ab7d696487ff96e8fa9d39de76c44515372f',
 'experiments/orthemology-v5-successors/source-store/28daa5deacd7358a75f1ccf7b2beededd4b323218dfd3c0dcde37c64415117e7/source-lock.json': '0af14f0df23408642214602e83cc3211efcda9a33a995a16865baa8cf23db025',
 'experiments/orthemology-v5-successors/source-store/44677823653e8e914ca7e8e4f582c08d6834bbe57c2835e8b0e4ddbca157eac8/SOURCE_IDENTITIES.json': 'd1f4442c116b50bcbe9ec172157bf192a8fd2d37eaed46c3d5a5d16803f1a58b',
 'experiments/orthemology-v5-successors/source-store/4c6d10a5d818dda9b5f68b8c8bdd6d9ec8a053e584e6aaa70e8c014cb49fbb14/DEPENDENCIES.json': '9d6524b06037093483f964a9d47633b2a003bd9ecce07f3bf9df581a90adf0e1',
 'experiments/orthemology-v5-successors/source-store/54638026fd05b40e780d1ed5d51bbd286398926e074b487f746237b5dd816be0/source-lock.json': 'bcf66ccc33db40b901b74b84d2611f990a7ebdd2d6c3b06d57e916463ace9410',
 'experiments/orthemology-v5-successors/source-store/59f9f607436e2b70ba2b8060aafcbf5edbd80f5c5c69553fe43447d039589924/lake-manifest.json': 'e766c35d157152fdd139d6bcd3443d430c8246be2549919a16b370cb3df14406',
 'experiments/orthemology-v5-successors/source-store/5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752/mathlib-lake-manifest.json': '7670c11c159257f2b7e79511e74024442764ccaea3ddd64e47df85ad195403da',
 'experiments/orthemology-v5-successors/source-store/5ca88d5793fb2283badb16c8d722b777e0e9eb49198043b9335a198d572060c7/MODULES.json': 'efe0a33ef9a4292a51d447dd55aa329f44bc4f315dcc7b60e3d4afbf51cbc580',
 'experiments/orthemology-v5-successors/source-store/72293db56804c56c017582d7d22f8dc21a985ab37ff258ac789160c2dfeb7c63/sense-source-lock.json': '36d38b458468f95cfc61671558ebe6a46a985d65c480783c6fbf384267448b84',
 'experiments/orthemology-v5-successors/source-store/7dc06e97812b481caac84ca86cc685c2fb255fdc119f650b83cc6851dc085e61/preserved-module-lock.json': '09bc31f615684c63eb5c00fa7ca7387b77619744690e7b641b3261e731278de4',
 'experiments/orthemology-v5-successors/source-store/8981fe18fb0d182dfbab01142f250354846dfb691c873d8d1ced71d3f1df3f4c/SOURCE_MANIFEST.json': 'e62e9d640e8a6204a02c49638c785ad9109e3995b962de4ba4f71512d098b694',
 'experiments/orthemology-v5-successors/source-store/95927e700cd403a2651b33280d052a8c972b12bca48c5cac26a1643c14a80cc6/VERIFICATION.json': 'e590599a732c26631a8cc10626bac0a0b091d869adc757bba1ff2bf7ca980642',
 'experiments/orthemology-v5-successors/source-store/9eaffaa788991447cf64938183de0e982b467d333dd9a369f11c0c99a0be595c/DEPENDENCY_PINS.json': 'aaa1405813e8ddbb86a2f630a5b7a4d44bfeeb89649ec37288ab4a54562fdfce',
 'experiments/orthemology-v5-successors/source-store/a774b663b6f6c6dfe81f7b6272cc57b8059a5bbfc7428ca4d0c41e0ba0fd88f2/TOOLCHAIN_REQUIREMENTS.json': '8aafe0be5934f2f02c118608afbc25dfc19e5bbaa8a0b48bd62f538efe5d632c',
 'experiments/orthemology-v5-successors/source-store/a919102c102ff3d07b447f52490266aca76afa4f84a972e2f3d78b3470f97a7a/INPUTS.json': 'ce885e003129dc6b65c8819498d6aee4314998a05ba1f6e563354057942a89af',
 'experiments/orthemology-v5-successors/source-store/b7500882ab904ebc84f3f28a036d687a54f5f023eac839b6177a1d65b679874f/INPUT_SOURCE_MANIFEST.json': '24672e5a3f2cc8d58a3f59635122a30926f510a02ede7949976ce5f36369e3e7',
 'experiments/orthemology-v5-successors/source-store/bd800ff0214d7a382feb5da185d706766185fa309794ab52b2ad9e26444f613c/source-lock.json': '47fee37425fe3aaab4d28c2206d573ae9eeeb8c18bd5fdd78efd839e743bc6b7',
 'experiments/orthemology-v5-successors/source-store/f7bda53cf932963883223c7f14f305b1354b35207d2a50da3c0dfcc2e3813eec/SOURCE_LOCK.json': '22673682c67f7715ab9049485187f9917e926aac6c28e93f3613bd9bbc164e8a',
 'experiments/orthemology-v5-successors/source-store/fc51e32962e76ac4c5ebef5c3154b5c4a1ab6061aeb018db712d128ee6dac210/CANDIDATE_v1.json': '5c4b8f56e2e550c5a80e7285d04d08dad69f4bbed3c8c342e8aa595933ed2e8e'}
SUCCESSOR_INPUT_PUBLIC_ROWS = {'experiments/orthemology-v5-successors/source-store/54638026fd05b40e780d1ed5d51bbd286398926e074b487f746237b5dd816be0/source-lock.json': '5e12a40c3ff8ca85d985c985d854241f99c608d8fa1b2fae3c1eb1d8d46eddb3',
 'experiments/orthemology-v5-successors/source-store/72293db56804c56c017582d7d22f8dc21a985ab37ff258ac789160c2dfeb7c63/sense-source-lock.json': 'd5e0f7b74663fb8a776d89b3e8c260548eb67b5ae4b6d4d5d9bb8e445d24545d',
 'experiments/orthemology-v5-successors/source-store/a919102c102ff3d07b447f52490266aca76afa4f84a972e2f3d78b3470f97a7a/INPUTS.json': '509a4a86b62e81850c4e7e1ea4ecbb3360b8a3753adf49c2c4ca8f0071ff95b9'}
SUCCESSOR_INPUT_REPLAY_ORIGINAL = ('8f6641df9d613c0814652a9b2fc338f72ebe2230',
 '5b4c1b7f0ced9af2599b980fd25fd1a15b819357853753319798b2965fc540ef',
 450007,
 '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')


def _successor_input_path(root, path):
    node = root / path
    for part in (root, *root.parents, *node.parents, node):
        try:
            if stat.S_ISLNK(part.lstat().st_mode):
                raise ValueError('consolidated input path contains a symlink: ' + path)
        except FileNotFoundError:
            continue
    return node


def _successor_input_regular(root, path):
    node = _successor_input_path(root, path)
    fields = ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
    with os.fdopen(os.open(node, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK), 'rb') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_mode & 0o111:
            raise ValueError('consolidated input source is not an ordinary nonexecutable file: ' + path)
        body = stream.read()
        after = os.fstat(stream.fileno())
    witness = tuple(getattr(before, field) for field in fields)
    current = node.lstat()
    if witness != tuple(getattr(after, field) for field in fields) or witness != tuple(getattr(current, field) for field in fields):
        raise ValueError('consolidated input source changed during read: ' + path)
    return body, witness


def _successor_input_catalog(root):
    root = pathlib.Path(root).absolute()
    _successor_input_path(root, SUCCESSOR_INPUT_REGISTRY)
    names = SUCCESSOR_INPUT_PATHS | {SUCCESSOR_INPUT_REGISTRY}
    arguments = ('ls-files', '--stage', '-z', '--', *sorted(names))
    before_index = _administrative_git(root, *arguments)
    entries = {}
    for item in before_index.split(b'\0'):
        if not item:
            continue
        try:
            meta, raw_path = item.split(b'\t', 1)
            mode, oid, stage = meta.decode('ascii').split()
            path = raw_path.decode('utf-8')
        except (ValueError, UnicodeError) as exc:
            raise ValueError('malformed consolidated input index') from exc
        if path not in names or path in entries or mode != '100644' or stage != '0':
            raise ValueError('consolidated input index path, mode or stage differs')
        entries[path] = oid
    registry_body, registry_witness = _successor_input_regular(root, SUCCESSOR_INPUT_REGISTRY)
    registry_oid = hashlib.sha1(b'blob ' + str(len(registry_body)).encode() + b'\0' + registry_body).hexdigest()
    registry_identity = (registry_oid, digest(registry_body), len(registry_body))
    if (registry_identity not in (SUCCESSOR_INPUT_REGISTRY_ORIGINAL, SUCCESSOR_INPUT_REGISTRY_COMPACT,
                                     SUCCESSOR_INPUT_REGISTRY_CALCULUS)
            or entries.get(SUCCESSOR_INPUT_REGISTRY) != registry_oid):
        raise ValueError('consolidated input registry has a changed or mixed native edition')
    registry = json.loads(registry_body)
    witnesses = {SUCCESSOR_INPUT_REGISTRY: registry_witness}
    originals = {}
    if registry_identity in (SUCCESSOR_INPUT_REGISTRY_COMPACT, SUCCESSOR_INPUT_REGISTRY_CALCULUS):
        content = registry.get('preserved_source_inputs')
        if not isinstance(content, dict) or set(content) != SUCCESSOR_INPUT_PATHS or not all(isinstance(value, str) for value in content.values()):
            raise ValueError('consolidated input registry has an incomplete finite population')
        originals = {path: value.encode('utf-8') for path, value in content.items()}
        old_registry = {key: value for key, value in registry.items() if key != 'preserved_source_inputs'}
        if registry_identity == SUCCESSOR_INPUT_REGISTRY_CALCULUS:
            old_registry['records'] = dict(old_registry['records'], CALCULUS_MAP={
                'path': SUCCESSOR_CALCULUS_MAP, 'sha256': SUCCESSOR_CALCULUS_MAP_IDENTITY[1]})
        original_registry_body = (json.dumps(old_registry, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()
    else:
        if 'preserved_source_inputs' in registry:
            raise ValueError('original registry unexpectedly contains the successor field')
        original_registry_body = registry_body
        for path in SUCCESSOR_INPUT_PATHS:
            originals[path], witnesses[path] = _successor_input_regular(root, path)
    original_oid = hashlib.sha1(b'blob ' + str(len(original_registry_body)).encode() + b'\0' + original_registry_body).hexdigest()
    if (original_oid, digest(original_registry_body), len(original_registry_body)) != SUCCESSOR_INPUT_REGISTRY_ORIGINAL:
        raise ValueError('consolidated registry changed an original programme/status/record field')
    absent = set()
    for path, expected in SUCCESSOR_INPUT_IDENTITIES.items():
        body = originals[path]
        oid = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        if (oid, digest(body), len(body)) != expected:
            raise ValueError('consolidated original input identity differs: ' + path)
        if path in entries and entries[path] != oid:
            raise ValueError('consolidated original input staged identity differs: ' + path)
        node = _successor_input_path(root, path)
        if os.path.lexists(node):
            present, witnesses[path] = _successor_input_regular(root, path)
            if present != body:
                raise ValueError('consolidated original input present bytes differ: ' + path)
        else:
            absent.add(path)
    if _administrative_git(root, *arguments) != before_index:
        raise ValueError('consolidated input native index changed during qualification')
    fields = ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
    for path, witness in witnesses.items():
        current = _successor_input_path(root, path).lstat()
        if tuple(getattr(current, field) for field in fields) != witness:
            raise ValueError('consolidated input changed during qualification: ' + path)
    if any(os.path.lexists(_successor_input_path(root, path)) for path in absent):
        raise ValueError('consolidated input absence changed during qualification')
    return originals, absent, original_registry_body, registry


def _successor_calculus_catalog(root):
    """Authenticate the one retired view against its unchanged live owners.

    This is historical byte recovery only. Current result, status and suite
    validation reads RESULT_STATUS directly and grants no adoption by recovery.
    """
    root = pathlib.Path(root).absolute()
    names = {SUCCESSOR_INPUT_REGISTRY, SUCCESSOR_CALCULUS_MAP,
             SUCCESSOR_CALCULUS_RESULTS, *SUCCESSOR_CALCULUS_GUIDES}
    arguments = ('ls-files', '--stage', '-z', '--', *sorted(names))
    before_index = _administrative_git(root, *arguments)
    entries = {}
    for item in before_index.split(b'\0'):
        if not item:
            continue
        try:
            meta, raw_path = item.split(b'\t', 1)
            mode, oid, stage = meta.decode('ascii').split()
            path = raw_path.decode('utf-8')
        except (ValueError, UnicodeError) as exc:
            raise ValueError('malformed calculus owner index') from exc
        if path not in names or path in entries or mode != '100644' or stage != '0':
            raise ValueError('calculus owner index path, mode or stage differs')
        entries[path] = oid
    registry_body, registry_witness = _successor_input_regular(root, SUCCESSOR_INPUT_REGISTRY)
    registry_oid = hashlib.sha1(b'blob ' + str(len(registry_body)).encode() + b'\0' + registry_body).hexdigest()
    if ((registry_oid, digest(registry_body), len(registry_body)) != SUCCESSOR_INPUT_REGISTRY_CALCULUS
            or entries.get(SUCCESSOR_INPUT_REGISTRY) != registry_oid):
        raise ValueError('calculus recovery requires the exact current registry edition')
    registry = _successor_input_catalog(root)[3]
    if registry['records'].get('RESULT_STATUS') != {
            'path': SUCCESSOR_CALCULUS_RESULTS, 'sha256': SUCCESSOR_CALCULUS_RESULT_IDENTITY[1]}:
        raise ValueError('calculus result owner binding differs')
    witnesses = {SUCCESSOR_INPUT_REGISTRY: registry_witness}
    bodies = {}
    originals = {}
    owners = {SUCCESSOR_CALCULUS_RESULTS: SUCCESSOR_CALCULUS_RESULT_IDENTITY,
              **{path: spec['current'] for path, spec in SUCCESSOR_CALCULUS_GUIDES.items()}}
    for path, expected in owners.items():
        body, witnesses[path] = _successor_input_regular(root, path)
        oid = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        if (oid, digest(body), len(body)) != expected or entries.get(path) != oid:
            raise ValueError('calculus live owner has changed or mixed native bytes: ' + path)
        bodies[path] = body
        if path in SUCCESSOR_CALCULUS_GUIDES:
            spec = SUCCESSOR_CALCULUS_GUIDES[path]
            current, original = spec['replacement'].encode(), spec['original_text'].encode()
            if body.count(current) != 1:
                raise ValueError('calculus guide inverse is ambiguous: ' + path)
            original_body = body.replace(current, original, 1)
            original_oid = hashlib.sha1(b'blob ' + str(len(original_body)).encode() + b'\0' + original_body).hexdigest()
            if (original_oid, digest(original_body), len(original_body)) != spec['original']:
                raise ValueError('calculus guide changed outside its reviewed link: ' + path)
            originals[path] = original_body
    result_document = json.loads(bodies[SUCCESSOR_CALCULUS_RESULTS])
    historical = {'results': [
        {'id': row['id'], 'calculus': row['calculus'],
         'operational_model': row['operational_model'], 'canonical_adoption': 'NOT_ADOPTED'}
        for row in result_document['results']]}
    body = (json.dumps(historical, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()
    oid = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
    if (oid, digest(body), len(body)) != SUCCESSOR_CALCULUS_MAP_IDENTITY:
        raise ValueError('calculus historical reconstruction differs from its original identity')
    if SUCCESSOR_CALCULUS_MAP in entries and entries[SUCCESSOR_CALCULUS_MAP] != oid:
        raise ValueError('calculus historical view has a changed staged identity')
    node = _successor_input_path(root, SUCCESSOR_CALCULUS_MAP)
    absent = set()
    if os.path.lexists(node):
        present, witnesses[SUCCESSOR_CALCULUS_MAP] = _successor_input_regular(root, SUCCESSOR_CALCULUS_MAP)
        if present != body:
            raise ValueError('calculus historical view has changed present bytes')
    else:
        absent.add(SUCCESSOR_CALCULUS_MAP)
    if _administrative_git(root, *arguments) != before_index:
        raise ValueError('calculus native index changed during qualification')
    fields = ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
    for path, witness in witnesses.items():
        current = _successor_input_path(root, path).lstat()
        if tuple(getattr(current, field) for field in fields) != witness:
            raise ValueError('calculus owner changed during qualification: ' + path)
    if absent and os.path.lexists(_successor_input_path(root, SUCCESSOR_CALCULUS_MAP)):
        raise ValueError('calculus historical absence changed during qualification')
    return body, absent, originals


def successor_calculus_map_bytes(root):
    """Return the exact original, non-adopting map for historical citations."""
    return _successor_calculus_catalog(root)[0]


def successor_calculus_map_absences(root):
    return _successor_calculus_catalog(root)[1]


def successor_calculus_guide_source_bytes(root, path):
    if path not in SUCCESSOR_CALCULUS_GUIDES:
        raise ValueError('path is outside the finite calculus navigation edits')
    return _successor_calculus_catalog(root)[2][path]


def successor_input_bytes(root, path):
    """Return one exact original public document from its current compact owner."""
    if path not in SUCCESSOR_INPUT_PATHS:
        raise ValueError('path is outside the finite consolidated input class')
    return _successor_input_catalog(root)[0][path]


def successor_input_absences(root):
    return _successor_input_catalog(root)[1]


def successor_input_registry_original_bytes(root):
    """Retain the discovery owner's exact original view after native admission."""
    return _successor_input_catalog(root)[2]


def successor_input_registry_document(root):
    return _successor_input_catalog(root)[3]


def _successor_input_row_identity(row):
    return digest(json.dumps(row, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode())


def successor_input_source_bytes(root, row):
    if (row.get('public_path') not in SUCCESSOR_INPUT_PATHS
            or SUCCESSOR_INPUT_SOURCE_ROWS.get(row.get('id')) != _successor_input_row_identity(row)):
        raise ValueError('consolidated input original source-ID/projection/review row differs')
    return successor_input_bytes(root, row['public_path'])


def successor_input_allowlist_bytes(root, row):
    if SUCCESSOR_INPUT_ALLOWLIST_ROWS.get(row.get('path')) != _successor_input_row_identity(row):
        raise ValueError('consolidated input original allowlist role/source association differs')
    return successor_input_bytes(root, row['path'])


def successor_input_public_bytes(root, row):
    if SUCCESSOR_INPUT_PUBLIC_ROWS.get(row.get('repository_path')) != _successor_input_row_identity(row):
        raise ValueError('consolidated input original public identity or role differs')
    return successor_input_bytes(root, row['repository_path'])


# The 75 public renderings and 48 negative-case copies have current compact
# owners. Their original bytes, roles and counterexamples remain exact. This
# route does not recover fixture bodies from Git, run a scorer or read keys.
# The finite path set and identity digest are the original public123 edition;
# the three ordinary current owners must also match their native index entries.
GENERATED_FIXTURE_OWNERS = {'experiments/episode-reification-v2/scripts/generate_cases.py': ('e43f016e6a12594c29deef253cf1ba65d86462be',
                                                                  '3b449a7580426fdf89f85612018473f92c3c2c274d4eea47e7046d1bcfe1bc89',
                                                                  9631),
 'experiments/episode-reification/scripts/generate_fixtures.py': ('be7dd10d2f60ad16c4cf9df2ea3316d778b0c8fc',
                                                                  '9c39be153165e8d1c5a074243fc5f4ba467862ccc0d433bb42e7471230e4b929',
                                                                  8675),
 'tests/schema-negative/NEGATIVE-FIXTURES.json': ('20b6e5801823e87db6b5fb1638d0e3992eee36e6',
                                                  'b229103cc93bb15d046cb15a1794d99d0cb40200fbc8fe9ac7ceff358c88d3e9',
                                                  108213)}
GENERATED_NEGATIVE_PATHS = frozenset(('tests/invalid/I01-empty-task-analysis.json',
 'tests/invalid/I02-empty-id-metaortheme.json',
 'tests/invalid/I03-duplicate-state-metaortheme.json',
 'tests/invalid/I04-bare-string-selector-metaortheme.json',
 'tests/invalid/I05-empty-anchor-metaorthemma.json',
 'tests/invalid/I06-plural-metaorthemma-type.json',
 'tests/invalid/I07-empty-metaorthemma-binding.json',
 'tests/invalid/I08-unresolved-residual-without-queue.json',
 'tests/invalid/I09-deferred-residual-without-trigger.json',
 'tests/invalid/I10-transferred-residual-without-receiver.json',
 'tests/invalid/I11-owner-assigned-residual-without-owner.json',
 'tests/invalid/I12-risk-accepted-residual-without-risk-record.json',
 'tests/invalid/I13-validated-resolved-without-evidence.json',
 'tests/invalid/I14-payload-free-handoff.json',
 'tests/invalid/I15-handoff-state-claim-without-valid-for-version.json',
 'tests/invalid/I16-skeletal-audit-ready-episode.json',
 'tests/invalid/I17-verdict-without-objectivity-index.json',
 'tests/invalid/I18-free-form-relspec.json',
 'tests/invalid/I19-free-form-perturbspec.json',
 'tests/invalid/I20-perturbspec-without-enumeration-or-measure.json',
 'tests/invalid/I21-verdict-missing-required-statuses.json',
 'tests/invalid/I22-na-without-reason-outside-required-path.json',
 'tests/invalid/I23-contradicted-pathway-summary.json',
 'tests/invalid/I24-claim-path-collapsed-into-episode-path.json',
 'tests/invalid/I25-relspec-declared-after-the-result.json',
 'tests/invalid/I26-perturbspec-invariant-also-varied.json',
 'tests/invalid/I27-claim-dependency-cycle.json',
 'tests/invalid/I28-token-anchored-to-another-occurrence.json',
 'tests/invalid/I29-analysis-self-inheritance.json',
 'tests/invalid/I30-analysis-inheritance-cycle.json',
 'tests/invalid/I31-analysis-unresolved-chain.json',
 'tests/invalid/I32-token-collision-across-episodes.json',
 'tests/invalid/I33-standalone-token-unowned.json',
 'tests/invalid/I34-token-scope-foreign-claim.json',
 'tests/invalid/I35-gc-ghost-mu-edition.json',
 'tests/invalid/I36-precedence-self-edge.json',
 'tests/invalid/I37-precedence-cycle.json',
 'tests/invalid/I38-token-outside-governing-config.json',
 'tests/invalid/I39-audit-ready-silent-external-analysis.json',
 'tests/invalid/I40-audit-ready-unresolved-external-ref.json',
 'tests/invalid/I41-mixed-offset-postdated-relspec.json',
 'tests/invalid/I42-naive-timestamp-relspec.json',
 'tests/invalid/I43-inverted-token-validity.json',
 'tests/invalid/I44-req-reason-omission.json',
 'tests/invalid/I45-naive-decision-time.json',
 'tests/invalid/I46-audit-ready-implicit-claim-type.json',
 'tests/invalid/I47-currency-exempt-undeclared-scope.json',
 'tests/invalid/I48-robustness-silently-disabled.json'))
GENERATED_FIXTURE_PATHS = GENERATED_NEGATIVE_PATHS | {
    'experiments/episode-reification/fixtures/E' + str(case) + '/' + name
    for case in range(1, 6)
    for name in ('baseline-log.md', 'facts.yaml', 'treatment-episode.json')
} | {
    'experiments/episode-reification-v2/fixtures/C' + format(case, '02d') + '/' + name
    for case in range(1, 21)
    for name in ('baseline-record.md', 'facts.json', 'treatment-record.json')
}
GENERATED_FIXTURE_IDENTITY_SHA256 = '2b078fcd3245db2e5b967145e00b1de4cb2bb5cfe2456f7f6c73d18de3e27540'


def _generated_fixture_path(root, name):
    target = root / name
    for path in (root, *root.parents, *target.parents, target):
        try:
            if stat.S_ISLNK(path.lstat().st_mode):
                raise ValueError('generated fixture source has a symlink component: ' + name)
        except FileNotFoundError:
            continue
    return target


def _generated_fixture_regular(root, name):
    target = _generated_fixture_path(root, name)
    fields = ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
    with os.fdopen(os.open(target, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK), 'rb') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_mode & 0o111:
            raise ValueError('generated fixture source is not an ordinary nonexecutable file: ' + name)
        body = stream.read()
        after = os.fstat(stream.fileno())
    witness = tuple(getattr(before, field) for field in fields)
    current_path = target.lstat()
    if (witness != tuple(getattr(after, field) for field in fields)
            or witness != tuple(getattr(current_path, field) for field in fields)):
        raise ValueError('generated fixture source changed during the ordinary read: ' + name)
    return body, witness


def _generated_fixture_index(root):
    environment = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
    environment.update(GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1', GIT_ALLOW_PROTOCOL='',
                       GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0', GIT_CONFIG_NOSYSTEM='1',
                       GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
    process = subprocess.run(
        ['/usr/bin/git', '--no-replace-objects', '--literal-pathspecs', 'ls-files', '--stage', '-z', '--',
         *sorted(GENERATED_FIXTURE_PATHS | GENERATED_FIXTURE_OWNERS.keys())],
        cwd=root, env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode:
        raise ValueError('generated fixture native index is unavailable')
    return process.stdout


def _generated_fixture_catalog(root):
    root = pathlib.Path(root).absolute()
    _generated_fixture_path(root, next(iter(GENERATED_FIXTURE_OWNERS)))
    originals = {}
    witnesses = {}
    before_index = _generated_fixture_index(root)
    entries = {}
    for entry in before_index.split(b'\0'):
        if not entry:
            continue
        try:
            metadata, raw_path = entry.split(b'\t', 1)
            mode, oid, stage = metadata.decode('ascii').split()
            name = raw_path.decode('utf-8')
        except (ValueError, UnicodeError) as exc:
            raise ValueError('malformed generated fixture index entry') from exc
        if name not in GENERATED_FIXTURE_PATHS | GENERATED_FIXTURE_OWNERS.keys() or name in entries:
            raise ValueError('unexpected or repeated generated fixture index entry')
        if mode != '100644' or stage != '0':
            raise ValueError('generated fixture index mode or stage differs: ' + name)
        entries[name] = oid
    for name, (oid, identity, size) in GENERATED_FIXTURE_OWNERS.items():
        if entries.get(name) != oid:
            raise ValueError('generated fixture owner is missing or differs in the native index: ' + name)
        body, witnesses[name] = _generated_fixture_regular(root, name)
        actual_oid = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        if (actual_oid, digest(body), len(body)) != (oid, identity, size):
            raise ValueError('generated fixture current owner bytes differ: ' + name)
        if name.endswith('.py'):
            # This is the already admitted pure public renderer, hash checked
            # before compilation. Neither main() nor scoring_keys() is called.
            namespace = {'__name__': 'episode_public_renderer', '__file__': str(root / name)}
            exec(compile(body, name, 'exec'), namespace)
            rendered = namespace['public_files']()
            if not isinstance(rendered, dict) or not all(
                    isinstance(path, str) and isinstance(text, str) for path, text in rendered.items()):
                raise ValueError('public fixture renderer returned an invalid mapping')
            prefix = name.split('/scripts/')[0] + '/fixtures/'
            materialized = {prefix + path: text.encode('utf-8') for path, text in rendered.items()}
        else:
            materialized = {}
            for row in json.loads(body)['invalid_fixtures']:
                path = 'tests/invalid/' + row['id'] + '.json'
                if path in materialized:
                    raise ValueError('repeated canonical negative case')
                materialized[path] = (json.dumps(row, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
        if set(originals) & set(materialized):
            raise ValueError('overlapping generated fixture owners')
        originals.update(materialized)
    if set(originals) != GENERATED_FIXTURE_PATHS:
        raise ValueError('generated fixture original population differs')
    identities = []
    for name, body in sorted(originals.items()):
        oid = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        identities.append([name, oid, digest(body), len(body)])
        if name in entries and entries[name] != oid:
            raise ValueError('generated fixture original staged identity differs: ' + name)
        target = _generated_fixture_path(root, name)
        if os.path.lexists(target):
            present, witnesses[name] = _generated_fixture_regular(root, name)
            if present != body:
                raise ValueError('generated fixture present original differs: ' + name)
        else:
            witnesses[name] = None
    if digest(json.dumps(identities, separators=(',', ':'), ensure_ascii=False).encode()) != GENERATED_FIXTURE_IDENTITY_SHA256:
        raise ValueError('generated fixture complete original identity binding differs')
    if _generated_fixture_index(root) != before_index:
        raise ValueError('generated fixture native index changed during qualification')
    fields = ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
    for name, witness in witnesses.items():
        target = _generated_fixture_path(root, name)
        if witness is None:
            if os.path.lexists(target):
                raise ValueError('absent generated fixture reappeared during qualification: ' + name)
        else:
            current_path = target.lstat()
            if tuple(getattr(current_path, field) for field in fields) != witness:
                raise ValueError('generated fixture source changed during qualification: ' + name)
    return originals, {name for name, witness in witnesses.items() if witness is None}


def generated_fixture_bytes(root, path):
    """Exact original bytes from current public generators/canonical cases only."""
    if path not in GENERATED_FIXTURE_PATHS:
        raise ValueError('path is outside the finite live-derived fixture class')
    return _generated_fixture_catalog(root)[0][path]


def generated_fixture_absences(root):
    """Only genuine missing originals with exact live owners qualify."""
    return _generated_fixture_catalog(root)[1]


def generated_fixture_source_bytes(root, row):
    path = row.get('repository_path')
    if path not in GENERATED_FIXTURE_PATHS:
        raise ValueError('public path is outside the finite live-derived fixture class')
    body = generated_fixture_bytes(root, path)
    argument = path.endswith('.md')
    expected = {
        'source_sha256': digest(body), 'source_action': 'include', 'source_bytes': len(body),
        'role': 'authored_argument' if argument else 'qualified_metadata',
        'declared_eligibility_basis': 'reviewed_owner_authored' if argument else 'reviewed_distribution_metadata',
        'required_dependencies': [], 'disposition': 'REUSE', 'repository_path': path,
        'public_sha256': digest(body), 'public_bytes': len(body),
        'publication_basis': 'exact_existing_public_repository_object',
    }
    if row != expected:
        raise ValueError('generated fixture public original identity, role or complete row differs')
    return body


def _formal_tuple_binding(values, count, expected):
    if len(values) != count or digest(json.dumps(values, separators=(',', ':')).encode()) != expected:
        raise ValueError('formal finite catalog differs')


def _formal_copy_catalog():
    """Bind71 original formal coordinates without changing their proof roles."""
    _formal_tuple_binding(FORMAL_COPY_MEMBERS, 71, FORMAL_COPY_MEMBERS_SHA256)
    result = {}
    for alias, canonical, blob, identity, size in FORMAL_COPY_MEMBERS:
        for path in (alias, canonical):
            if (not isinstance(path, str) or not path.endswith('.lean')
                    or not path.startswith(('experiments/orthemology-v5/',
                        'experiments/orthemology-v5-continuations/', 'experiments/orthemology-v5-successors/',
                        'research/t20-live-20261009/'))
                    or '\\' in path or '\0' in path or ':' in path
                    or any(part in ('', '.', '..', '.git') for part in path.split('/'))):
                raise ValueError('formal source coordinate differs')
        if (alias == canonical or alias in result or not re.fullmatch(r'[0-9a-f]{40}', blob)
                or not re.fullmatch(r'[0-9a-f]{64}', identity) or type(size) is not int or size <= 0):
            raise ValueError('formal source identity differs')
        result[alias] = {'canonical': canonical, 'blob': blob, 'sha256': identity, 'bytes': size, 'mode': '100644'}
    kept = {r['canonical'] for r in result.values()}
    if (len(result) != 71 or len(kept) != 37 or set(result) & kept
            or FORMAL_COPY_PATHS != frozenset(result)
            or len(FORMAL_CONTINUATION_PATHS) != 6 or len(FORMAL_SUCCESSOR_PATHS) != 3
            or not FORMAL_CONTINUATION_PATHS < set(result) or not FORMAL_SUCCESSOR_PATHS < set(result)
            or FORMAL_CONTINUATION_PATHS & FORMAL_SUCCESSOR_PATHS
            or set(result) & (CHECKPOINT_COPY_PATHS | CHECKPOINT_RECORD_COPY_PATHS | CHECKPOINT_PACKAGE_COPY_PATHS)):
        raise ValueError('formal retained population differs')
    return result


def _formal_current_provider_catalog():
    """Join six ordinary destinations to their unchanged original source identities."""
    _formal_tuple_binding(FORMAL_CURRENT_PROVIDERS, 6, FORMAL_CURRENT_PROVIDERS_SHA256)
    original = _formal_copy_catalog()
    result, destinations = {}, set()
    for canonical, current in FORMAL_CURRENT_PROVIDERS:
        if (canonical in result or current in destinations
                or not current.startswith('formal/certificate-frontier/')
                or not current.endswith('.lean') or '\\' in current or '\0' in current
                or any(part in ('', '.', '..', '.git') for part in current.split('/'))):
            raise ValueError('formal current provider coordinate differs')
        matches = [binding for binding in original.values() if binding['canonical'] == canonical]
        if not matches or any(binding != matches[0] for binding in matches):
            raise ValueError('formal original provider identity differs')
        result[canonical] = dict(matches[0], current=current)
        destinations.add(current)
    if (len(result) != 6 or len(destinations) != 6
            or sum(binding['canonical'] in result for binding in original.values()) != 16):
        raise ValueError('formal current provider population differs')
    return result


def formal_copy_bytes(root, path, identity=None, size=None):
    """Read exact current bytes while retaining each original native coordinate."""
    # Validate the complete dispatch before deciding which source route applies.
    original = _formal_copy_catalog()
    providers = _formal_current_provider_catalog()
    if not isinstance(path, str):
        raise ValueError('unqualified formal source path')
    if path in original:
        binding = original[path]
    else:
        selected = [row for canonical, row in providers.items()
                    if path in (canonical, row['current'])]
        if len(selected) != 1:
            raise ValueError('unqualified formal source path')
        binding = {key: value for key, value in selected[0].items() if key != 'current'}
        path = binding['canonical']
    if ((identity is not None and identity != binding['sha256'])
            or (size is not None and size != binding['bytes'])):
        raise ValueError('formal requested identity differs')
    current = providers.get(binding['canonical'], {}).get('current')
    return _checkpoint_bound_bytes(root, path, binding, current=current)


def formal_provider_absences(root):
    """Authenticate all six migrated providers before returning actual old absences."""
    result = set()
    for canonical in _formal_current_provider_catalog():
        formal_copy_bytes(root, canonical)
        if not os.path.lexists(pathlib.Path(root) / canonical):
            result.add(canonical)
    return result


def formal_duplicate_paths(root):
    """Authenticate the complete class before admitting actual source absences."""
    result = set()
    for path, binding in _formal_copy_catalog().items():
        formal_copy_bytes(root, path)
        if not os.path.lexists(pathlib.Path(root) / path):
            result.add(path)
    return result


def continuation_formal_current_paths():
    """Validate the exact guard dispatch before any ordinary-source decision."""
    _formal_tuple_binding(CONTINUATION_FORMAL_RETARGETS, 1, CONTINUATION_FORMAL_RETARGETS_SHA256)
    if (CONTINUATION_FORMAL_RETARGET_PATHS != frozenset(r[0] for r in CONTINUATION_FORMAL_RETARGETS)
            or CONTINUATION_FORMAL_CURRENT_PATHS != {
                'formal/type-theory/' + pathlib.PurePosixPath(r[2]).name: r[0]
                for r in CONTINUATION_FORMAL_RETARGETS}):
        raise ValueError('formal prior-provider population differs')
    return CONTINUATION_FORMAL_CURRENT_PATHS


def _continuation_formal_bound_bytes(root, path, binding):
    """Preserve the legacy source rows and two anchors across one provider chain."""
    continuation_formal_current_paths()
    if path not in CONTINUATION_FORMAL_RETARGET_PATHS:
        return _continuation_bound_bytes(root, path, binding)
    alias, former, canonical, blob, identity, size = CONTINUATION_FORMAL_RETARGETS[0]
    expected = {'canonical': canonical, 'blob': blob, 'sha256': identity, 'bytes': size, 'mode': '100644'}
    if (path != alias or _formal_copy_catalog().get(former) != expected
            or binding.get('canonical') != former
            or (binding.get('blob'), binding.get('sha256'), binding.get('bytes')) != (blob, identity, size)):
        raise ValueError('formal prior-provider identity differs')
    # A correct endpoint cannot conceal a corrupt present/staged former provider.
    current = 'formal/type-theory/' + pathlib.PurePosixPath(canonical).name
    _checkpoint_bound_bytes(root, former, expected, current=current)
    return _continuation_bound_bytes(root, path, dict(binding, canonical=canonical), current=current)


def _formal_row_digest(row):
    return digest(json.dumps(row, sort_keys=True, ensure_ascii=False,
                             separators=(',', ':'), allow_nan=False).encode('utf-8'))


def _formal_source_row_bytes(root, row, continuation):
    if not isinstance(row, dict):
        raise ValueError('formal source row is not an object')
    if continuation:
        values, count, expected = FORMAL_CONTINUATION_SOURCE_MEMBERS, 12, FORMAL_CONTINUATION_SOURCE_MEMBERS_SHA256
        path_key, identity_key, size_key, paths = 'path', 'sha256', 'bytes', FORMAL_CONTINUATION_PATHS
    else:
        values, count, expected = FORMAL_SUCCESSOR_SOURCE_MEMBERS, 9, FORMAL_SUCCESSOR_SOURCE_MEMBERS_SHA256
        path_key, identity_key, size_key, paths = 'public_path', 'public_sha256', 'public_bytes', FORMAL_SUCCESSOR_PATHS
    _formal_tuple_binding(values, count, expected)
    members = {key: (path, identity) for key, path, identity in values}
    if (len(members) != count or frozenset(path for path, _ in members.values()) != paths
            or row.get(path_key) not in paths
            or members.get(row.get('id')) != (row.get(path_key), _formal_row_digest(row))):
        raise ValueError('formal full source-ID/provenance row differs')
    return formal_copy_bytes(root, row[path_key], row[identity_key], row[size_key])


def continuation_formal_source_bytes(root, row):
    """Keep all twelve original origin/member/source-ID bindings unchanged."""
    return _formal_source_row_bytes(root, row, True)


def successor_formal_source_bytes(root, row):
    """Keep all nine original source IDs and complete provenance contracts."""
    return _formal_source_row_bytes(root, row, False)


def successor_formal_allowlist_bytes(root, row):
    _formal_tuple_binding(FORMAL_SUCCESSOR_ALLOWLIST_MEMBERS, 3, FORMAL_SUCCESSOR_ALLOWLIST_MEMBERS_SHA256)
    members = dict(FORMAL_SUCCESSOR_ALLOWLIST_MEMBERS)
    if (len(members) != 3 or frozenset(members) != FORMAL_SUCCESSOR_PATHS
            or not isinstance(row, dict) or row.get('path') not in members
            or members[row['path']] != _formal_row_digest(row)):
        raise ValueError('formal allowlist kind/source associations differ')
    return formal_copy_bytes(root, row['path'], row['sha256'], row['bytes'])


def _formal_public_source_bytes(root, row):
    _formal_tuple_binding(FORMAL_PUBLIC_MEMBERS, 27, FORMAL_PUBLIC_MEMBERS_SHA256)
    members = dict(FORMAL_PUBLIC_MEMBERS)
    if (len(members) != 27 or len(set(members) & FORMAL_COPY_PATHS) != 26
            or set(members) - FORMAL_COPY_PATHS != CONTINUATION_FORMAL_RETARGET_PATHS
            or not isinstance(row, dict) or row.get('repository_path') not in members
            or members[row['repository_path']] != _formal_row_digest(row)):
        raise ValueError('formal existing public role or complete identity differs')
    path = row['repository_path']
    if path in CONTINUATION_FORMAL_RETARGET_PATHS:
        return continuation_copy_bytes(root, path, row['public_sha256'], row['public_bytes'])
    return formal_copy_bytes(root, path, row['public_sha256'], row['public_bytes'])


def continuation_registry_source_bytes(root, row):
    """Keep one original public registry and its complete current owner edition.

    The existing preservation owner authenticates all four present owners and
    their index entries. The T20 row separately binds the original native Git
    coordinate; neither edition can stand in for a failed check of the other.
    """
    import validate_v5_successors as owners
    path = CONTINUATION_REGISTRY_PATH
    blob, identity, size = owners.PRESERVATION_OWNER_ORIGINAL[path]
    if (row.get('repository_path') != path or row.get('disposition') != 'REUSE'
            or row.get('repository_revision') != CONTINUATION_REGISTRY_REVISION
            or row.get('git_blob') != blob or row.get('source_sha256') != identity
            or row.get('public_sha256') != identity
            or row.get('source_bytes') != size or row.get('public_bytes') != size):
        raise ValueError('continuation registry public source owner differs')
    original_owners = {
        name: {'path': name, 'bytes': length, 'sha256': sha, 'git_blob_sha1': oid}
        for name, (oid, sha, length) in owners.PRESERVATION_OWNER_ORIGINAL.items()}
    originals = owners._preservation_owner_bytes(root, original_owners)
    _continuation_object(root, 'commit', CONTINUATION_REGISTRY_REVISION)
    expected = ('100644 blob ' + blob + '\t' + path + '\0').encode()
    if _continuation_git(root, 'ls-tree', '-z', CONTINUATION_REGISTRY_REVISION,
                         '--', path) != expected:
        raise ValueError('continuation registry historical path, mode or blob differs')
    body = _continuation_object(root, 'blob', blob)
    if ((len(body), digest(body)) != (size, identity)
            or (originals and originals[path] != body)):
        raise ValueError('continuation registry historical bytes differ')
    return body


SUCCESSOR_FIXTURE_PATH = 'tests/v5_successor_fixtures.py'
SUCCESSOR_FIXTURE_PUBLIC_ROW = {
    'source_sha256': '283ea7d698a5bf6a208e45260ee9078f819ecdb25a42c6dd2252d794d2dd3233',
    'source_action': 'include', 'source_bytes': 13030, 'role': 'authored_code',
    'declared_eligibility_basis': 'reviewed_owner_authored', 'required_dependencies': [],
    'disposition': 'REUSE', 'repository_path': SUCCESSOR_FIXTURE_PATH,
    'repository_revision': '69f3f9284f2cb94433958c0669fc9b06a9760fe7',
    'git_blob': 'ccf0bd64f34b10f65ed8bd1bdd8a88adcaf03c7f',
    'public_sha256': '283ea7d698a5bf6a208e45260ee9078f819ecdb25a42c6dd2252d794d2dd3233',
    'public_bytes': 13030, 'publication_basis': 'exact_existing_public_repository_object',
}
# The already-reviewed current fixture removes only its obsolete CALCULUS_MAP
# entry and two-line calculus field; the historical public row stays unchanged.
SUCCESSOR_FIXTURE_CURRENT = (
    '350c192a7c912232889673110d326e4242bde8cf',
    'd1b092a7deb91b71812f838d87d4af8de37fc72184b84eff8e8348d743ac0fb7', 12785)


def successor_fixture_source_bytes(root, row):
    """Return one immutable historical fixture view; never execute its body."""
    expected = SUCCESSOR_FIXTURE_PUBLIC_ROW
    if (type(row) is not dict or set(row) != set(expected)
            or any(type(row[key]) is not type(value) or row[key] != value
                   for key, value in expected.items())):
        raise ValueError('successor fixture public row differs')
    root = pathlib.Path(root)
    path = SUCCESSOR_FIXTURE_PATH
    current, witness = _successor_input_regular(root, path)
    original_identity = (expected['git_blob'], expected['public_sha256'], expected['public_bytes'])
    current_identity = (hashlib.sha1(b'blob ' + str(len(current)).encode() + b'\0' + current).hexdigest(),
                        digest(current), len(current))
    if current_identity not in (original_identity, SUCCESSOR_FIXTURE_CURRENT):
        raise ValueError('successor fixture current edition differs')
    environment = dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1',
                       GIT_ALLOW_PROTOCOL='', GIT_TERMINAL_PROMPT='0')

    def git(*args):
        result = subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs', *args],
                                cwd=root, capture_output=True, check=False, env=environment)
        if result.returncode:
            raise ValueError('successor fixture native identity unavailable')
        return result.stdout

    staged = git('ls-files', '--stage', '-z', '--', path)
    if staged != ('100644 ' + current_identity[0] + ' 0\t' + path + '\0').encode():
        raise ValueError('successor fixture current index differs')
    revision, blob = expected['repository_revision'], expected['git_blob']
    if git('cat-file', '-t', revision) != b'commit\n':
        raise ValueError('successor fixture historical revision is not a commit')
    if git('ls-tree', '-z', revision, '--', path) != ('100644 blob ' + blob + '\t' + path + '\0').encode():
        raise ValueError('successor fixture historical path, mode or blob differs')
    body = git('cat-file', 'blob', blob)
    identity = (hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest(),
                digest(body), len(body))
    if identity != original_identity:
        raise ValueError('successor fixture historical body differs')
    if git('ls-files', '--stage', '-z', '--', path) != staged:
        raise ValueError('successor fixture current index changed during historical read')
    repeated, repeated_witness = _successor_input_regular(root, path)
    if repeated_witness != witness or repeated != current:
        raise ValueError('successor fixture current source changed during historical read')
    return body


def source_bytes(root, row):
    path = pathlib.PurePosixPath(row['repository_path'])
    if path.is_absolute() or '..' in path.parts or '\\' in str(path):
        raise ValueError('unsafe source path')
    if str(path) in DIGEST_RECORD_PATHS:
        body = digest_record_public_bytes(root, row)
    elif str(path) == SUCCESSOR_FIXTURE_PATH:
        body = successor_fixture_source_bytes(root, row)
    elif is_binding_record(root, str(path)):
        body = binding_record_public_bytes(root, row)
    elif str(path) in SUCCESSOR_INPUT_PATHS:
        body = successor_input_public_bytes(root, row)
    elif str(path) in GENERATED_FIXTURE_PATHS:
        body = generated_fixture_source_bytes(root, row)
    elif str(path) == CONTINUATION_REGISTRY_PATH:
        body = continuation_registry_source_bytes(root, row)
    elif str(path) in FORMAL_COPY_PATHS or str(path) in CONTINUATION_FORMAL_RETARGET_PATHS:
        body = _formal_public_source_bytes(root, row)
    elif str(path) in ADMIN_PUBLIC_GUIDE_PATHS and row.get('repository_revision'):
        blob, identity, size, _ = ADMIN_GUIDES[str(path)]
        if (row.get('repository_revision') != ADMIN_RECORD_BASE or row.get('git_blob') != blob
                or row.get('disposition') != 'REUSE' or row.get('source_sha256') != identity
                or row.get('public_sha256') != identity or row.get('source_bytes') != size
                or row.get('public_bytes') != size):
            raise ValueError('administrative guide public historical identity differs')
        body = administrative_guide_source_bytes(root, str(path))
    elif str(path) in HISTORICAL_PROSE:
        blob, identity, size = HISTORICAL_PROSE[str(path)]
        if (row['repository_path'] != str(path) or str(path) not in HISTORICAL_PROSE_PUBLIC_PATHS
                or row.get('disposition') != HISTORICAL_PROSE_DISPOSITIONS[str(path)]
                or row.get('source_sha256') != identity or row.get('source_bytes') != size):
            raise ValueError('historical public source owner differs')
        body = historical_source_bytes(root, str(path), row.get('repository_revision'), row.get('git_blob'))
    elif str(path) in CHECKPOINT_CODE_COPY_PATHS:
        binding = _checkpoint_code_copy_catalog()[str(path)]
        if (str(path) not in CHECKPOINT_CODE_PUBLIC_PATHS or row['repository_path'] != str(path)
                or row.get('disposition') != 'REUSE' or row.get('role') != 'authored_code'
                or row.get('source_action') != 'include'
                or row.get('repository_revision') is not None or row.get('git_blob') is not None
                or row.get('source_sha256') != binding['sha256']
                or row.get('public_sha256') != binding['sha256']
                or row.get('source_bytes') != binding['bytes']
                or row.get('public_bytes') != binding['bytes']):
            raise ValueError('checkpoint code public identity or role differs')
        body = checkpoint_code_copy_bytes(root, str(path), row['public_sha256'], row['public_bytes'])
    elif str(path) in CHECKPOINT_RECORD_COPY_PATHS:
        binding = _checkpoint_record_copy_catalog()[str(path)]
        if (row['repository_path'] != str(path) or row.get('disposition') != 'REUSE'
                or row.get('repository_revision') is not None or row.get('git_blob') is not None
                or row.get('source_sha256') != binding['sha256']
                or row.get('public_sha256') != binding['sha256']
                or row.get('source_bytes') != binding['bytes']
                or row.get('public_bytes') != binding['bytes']):
            raise ValueError('checkpoint record public identity or role differs')
        body = checkpoint_record_copy_bytes(root, str(path), row['public_sha256'], row['public_bytes'])
    elif str(path) in CHECKPOINT_COPY_PATHS:
        binding = _checkpoint_copy_catalog()[str(path)]
        if (row['repository_path'] != str(path)
                or row.get('repository_revision') is not None or row.get('disposition') != 'REUSE'
                or row.get('git_blob') != binding['blob']
                or row.get('source_sha256') != row.get('public_sha256')
                or row.get('source_bytes') != row.get('public_bytes')):
            raise ValueError('checkpoint public source identity or role differs')
        body = checkpoint_copy_bytes(root, str(path), row['public_sha256'], row['public_bytes'])
    elif str(path).startswith(CONTINUATION_COPY_ROOT) and str(path).endswith('.lean'):
        if row.get('repository_revision') is not None:
            raise ValueError('current continuation copy cannot use historical reuse')
        if not os.path.lexists(root / path):
            if (row.get('disposition') != 'REUSE' or row.get('source_sha256') != row.get('public_sha256')
                    or row.get('source_bytes') != row.get('public_bytes')):
                raise ValueError('continuation public source identity differs')
            body = continuation_copy_bytes(root, str(path), row['public_sha256'], row['public_bytes'])
        else:
            body = _regular_current_bytes(root, str(path))
    elif row.get('repository_revision'):
        if row['repository_revision'] != HISTORICAL_PROSE_REVISION:
            raise ValueError('invalid pinned historical reuse')
        body = subprocess.check_output(['git', 'show', row['repository_revision'] + ':' + str(path)], cwd=root)
    else:
        target = root / path
        if target.is_symlink() or not target.resolve().is_relative_to(root.resolve()):
            raise ValueError('unsafe source target')
        body = target.read_bytes()
    if digest(body) != row['public_sha256'] or len(body) != row['public_bytes']:
        raise ValueError('source identity differs: ' + row['source_sha256'])
    return body


def lean_imports(text):
    """Read import commands, masking nested Lean comments and strings."""
    out = list(text)
    i, depth, quoted = 0, 0, False
    while i < len(text):
        if depth:
            if text.startswith('/-', i):
                depth += 1
                out[i:i+2] = '  '
                i += 2
            elif text.startswith('-/', i):
                depth -= 1
                out[i:i+2] = '  '
                i += 2
            else:
                if text[i] != '\n':
                    out[i] = ' '
                i += 1
        elif quoted:
            if text[i] == '\\' and i + 1 < len(text):
                out[i:i+2] = '  '
                i += 2
            else:
                quoted = text[i] != '"'
                if text[i] != '\n':
                    out[i] = ' '
                i += 1
        elif text.startswith('/-', i):
            depth = 1
            out[i:i+2] = '  '
            i += 2
        elif text.startswith('--', i):
            end = text.find('\n', i)
            end = len(text) if end < 0 else end
            out[i:end] = ' ' * (end-i)
            i = end
        elif text[i] == '"':
            quoted = True
            out[i] = ' '
            i += 1
        else:
            i += 1
    imports = []
    for line_number, line in enumerate(''.join(out).splitlines(), 1):
        match = re.match(r'^\s*import\s+(.+)$', line)
        if match:
            for module in match[1].split():
                if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.]*', module):
                    raise ValueError('unsupported Lean import syntax')
                imports.append((line_number, module))
    return imports


def closure(graph, root_hash):
    edges = collections.defaultdict(list)
    for edge in graph['edges']:
        edges[edge['parent_sha256']].append(edge['target_sha256'])
    seen, active, ordered = set(), set(), []

    def visit(identity):
        if identity in active:
            raise ValueError('cyclic custom import graph')
        if identity in seen:
            return
        active.add(identity)
        for child in edges[identity]:
            visit(child)
        active.remove(identity)
        seen.add(identity)
        ordered.append(identity)

    visit(root_hash)
    return ordered


def validate_graph(root, objects):
    errors = []
    graph_bytes = (root / PREFIX / 'CURRENT_SOURCE_GRAPH.json').read_bytes()
    graph = json.loads(graph_bytes)
    if digest(graph_bytes) != CURRENT_GRAPH_SHA256:
        errors.append('qualified current source graph differs')
    nodes = {n['source_sha256']: n for n in graph['nodes']}
    if len(nodes) != len(graph['nodes']):
        errors.append('duplicate current source node')
    declarations = collections.defaultdict(list)
    for edge in graph['edges']:
        parent, target = edge['parent_sha256'], edge['target_sha256']
        declarations[parent].append((edge['line'], edge['module']))
        if target not in nodes or edge['module'] not in nodes[target]['modules']:
            errors.append('custom import module binding differs: ' + parent)
        if objects.get(target, {}).get('disposition') not in PUBLIC:
            errors.append('required current source unavailable: ' + target)
    for edge in graph['official_import_edges']:
        declarations[edge['parent_sha256']].append((edge['line'], edge['module']))
        if edge['module'].split('.')[0] not in ('Init', 'Lean', 'Std', 'Mathlib'):
            errors.append('unqualified official import')
    for identity in nodes:
        row = objects.get(identity, {})
        if row.get('disposition') not in PUBLIC:
            errors.append('required current source unavailable: ' + identity)
            continue
        try:
            body = source_bytes(root, row)
            if digest(body) != identity:
                errors.append('current formal source must retain exact original bytes: ' + identity)
            actual = lean_imports(body.decode('utf-8'))
            if collections.Counter(actual) != collections.Counter(declarations[identity]):
                errors.append('actual import declarations differ: ' + identity)
        except (OSError, ValueError, KeyError, subprocess.CalledProcessError):
            errors.append('missing or changed current source: ' + identity)
    if set(declarations) - set(nodes):
        errors.append('import parent absent from source graph')
    reached = set()
    for suite in graph['suites']:
        ordered = closure(graph, suite['root_sha256'])
        reached.update(ordered)
        mapping = suite['modules']
        if any(not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*', module) for module in mapping):
            errors.append('unsafe suite module name: ' + suite['id'])
        if set(mapping.values()) != set(ordered) or len(mapping) != len(ordered):
            errors.append('isolated suite coverage differs: ' + suite['id'])
        if any(module not in nodes.get(identity, {}).get('modules', []) for module, identity in mapping.items()):
            errors.append('isolated suite module binding differs: ' + suite['id'])
        for edge in graph['edges']:
            if edge['parent_sha256'] in ordered and mapping.get(edge['module']) != edge['target_sha256']:
                errors.append('isolated suite imports a different variant: ' + suite['id'])
    if reached != set(nodes):
        errors.append('current source graph contains missing or unrooted nodes')
    for edge in graph['ordinary_proof_dependencies']:
        for key in ('parent_sha256', 'target_sha256'):
            if objects.get(edge[key], {}).get('disposition') not in PUBLIC:
                errors.append('ordinary proof support unavailable: ' + edge[key])
        try:
            body = source_bytes(root, objects[edge['parent_sha256']]).decode('utf-8')
            if edge['evidence_text'] not in body:
                errors.append('ordinary proof evidence binding differs: ' + edge['parent_sha256'])
        except (OSError, ValueError, KeyError):
            errors.append('ordinary proof parent unavailable: ' + edge['parent_sha256'])
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('find').add_argument('query')
    sub.add_parser('resolve').add_argument('source_sha256')
    export = sub.add_parser('export-suite')
    export.add_argument('suite')
    export.add_argument('destination', type=pathlib.Path)
    args = parser.parse_args()
    document = json.loads((ROOT / PREFIX / 'PUBLIC_PROJECTION_MANIFEST.json').read_bytes())
    objects = {r['source_sha256']: r for r in document['objects']}
    if args.command == 'find':
        query = args.query.casefold()
        for row in objects.values():
            if query in ' '.join([row['source_sha256'], row.get('repository_path', ''), *row.get('source_names', [])]).casefold():
                print(json.dumps(row, ensure_ascii=False))
    elif args.command == 'resolve':
        row = objects[args.source_sha256.removeprefix('source-sha256:')]
        if row['disposition'] in PUBLIC:
            source_bytes(ROOT, row)
        print(json.dumps(row, ensure_ascii=False, indent=2))
    else:
        errors = validate_graph(ROOT, objects)
        if errors:
            raise SystemExit('\n'.join(errors))
        graph = json.loads((ROOT / PREFIX / 'CURRENT_SOURCE_GRAPH.json').read_bytes())
        suite = next(s for s in graph['suites'] if s['id'] == args.suite)
        destination = args.destination.resolve()
        if destination.is_relative_to(ROOT):
            raise SystemExit('Reconstruct outside the repository in a fresh directory')
        # Verify all bytes before creating the fresh destination.
        modules = {identity: module for module, identity in suite['modules'].items()}
        plan = [(modules[h], source_bytes(ROOT, objects[h])) for h in closure(graph, suite['root_sha256'])]
        destination.mkdir(parents=True, exist_ok=False)
        for module, body in plan:
            path = destination / (module.replace('.', '/') + '.lean')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        (destination / 'REPLAY_ORDER.txt').write_text('\n'.join(m.replace('.', '/') for m, _ in plan) + '\n')
        (destination / 'RECONSTRUCTION.json').write_text(json.dumps(suite, indent=2) + '\n')
        print(json.dumps({'suite': suite['id'], 'verified_sources': len(plan), 'executed': False}))


if __name__ == '__main__':
    main()
