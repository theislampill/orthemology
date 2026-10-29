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
CONTINUATION_COPY_METADATA = {'docs/provenance/v5-research-continuations/SOURCE_MAP.json': (5960211,
                                                               'b434046568c41e56d060282975e7e7829bbed77b85bfb4e47108e9810da93384'),
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
        path = row.get('path') or ''
        if re.fullmatch(re.escape(CONTINUATION_COPY_ROOT) + r'[0-9a-f]{64}\.lean', path):
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


def _continuation_bound_bytes(root, path, binding):
    root = pathlib.Path(root)
    canonical, blob = binding['canonical'], binding['blob']
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
    body = _regular_current_bytes(root, canonical)
    if (len(body), digest(body)) != (binding['bytes'], binding['sha256']) or original != body:
        raise ValueError('continuation retained copy or original Git bytes differ')
    indexed = collections.defaultdict(list)
    for raw in _continuation_git(root, 'ls-files', '--stage', '-z', '--', path, canonical).split(b'\0'):
        if raw:
            metadata, name = raw.split(b'\t', 1)
            indexed[name.decode()].append(metadata.decode())
    expected = ['100644 ' + blob + ' 0']
    if indexed[path] not in ([], expected) or indexed[canonical] != expected:
        raise ValueError('continuation copy staged identity differs')
    target = root
    for part in path.split('/'):
        target = target / part
        if target.is_symlink():
            raise ValueError('continuation original path contains a symlink')
    if os.path.lexists(target) and _regular_current_bytes(root, path) != body:
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
    return _continuation_bound_bytes(root, path, binding)


def continuation_duplicate_paths(root):
    """Return only actual absences authenticated by the finite current-copy rule."""
    result = set()
    for path, binding in _continuation_copy_catalog(root).items():
        if not os.path.lexists(pathlib.Path(root) / path):
            _continuation_bound_bytes(root, path, binding)
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


def _checkpoint_bound_bytes(root, path, binding):
    """Authenticate one original coordinate and its exact retained public body."""
    root = pathlib.Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('checkpoint copy requires an ordinary repository root')
    canonical, blob = binding['canonical'], binding['blob']
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
        body = _regular_current_bytes(root, canonical)
        if (len(body), digest(body)) != (binding['bytes'], binding['sha256']) or body != original:
            raise ValueError('checkpoint retained body or original Git bytes differ')
        indexed = collections.defaultdict(list)
        for raw in _continuation_git(root, 'ls-files', '--stage', '-z',
                                     '--', path, canonical).split(b'\0'):
            if raw:
                metadata, name = raw.split(b'\t', 1)
                indexed[name.decode()].append(metadata.decode())
        expected_index = ['100644 ' + blob + ' 0']
        if indexed[path] not in ([], expected_index) or indexed[canonical] != expected_index:
            raise ValueError('checkpoint copy staged identity differs')
        target = root
        for part in path.split('/'):
            target = target / part
            if target.is_symlink():
                raise ValueError('checkpoint original path contains a symlink')
        if os.path.lexists(target) and _regular_current_bytes(root, path) != body:
            raise ValueError('present checkpoint original differs')
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


def source_bytes(root, row):
    path = pathlib.PurePosixPath(row['repository_path'])
    if path.is_absolute() or '..' in path.parts or '\\' in str(path):
        raise ValueError('unsafe source path')
    if str(path) == CONTINUATION_REGISTRY_PATH:
        body = continuation_registry_source_bytes(root, row)
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
