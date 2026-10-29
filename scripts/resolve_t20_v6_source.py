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
CONTINUATION_COPY_METADATA = {
    'docs/provenance/v5-research-continuations/SOURCE_MAP.json':
        (5976495, 'd65e5e79cf6be367f3d22296403d30be96b191ed1f68be1ca95ccff5b7676133'),
    'docs/provenance/v5-successors/SOURCE_MAP.json':
        (4978847, 'db90ad110ccc9c6a63454cf91ecec4605eed7fe243d18883d3cf501c58cb4883'),
    'docs/provenance/v5-successors/PRESERVATION.json':
        (379708, 'cd81d3b80d5183c1c01b637207d0afefd2b143ce4ee346808ca473a15eea6c4a'),
}


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
# by the existing crosswalk; these are not new T20 public manifest forms.
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
    if path != 'research/t20-live-20261009/checkpoints/CP20/necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md'
    and path not in CONTINUATION_READER_PROSE and path not in T4_READER_PROSE)


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
                or len(bindings) != len(HISTORICAL_PROSE)
                or {row['path'] for row in bindings} != set(HISTORICAL_PROSE)):
            raise ValueError('the exact earlier sixteen and ten T4 bindings are required')
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
                    (set(CONTINUATION_READER_HISTORICAL_PATHS), set(HISTORICAL_PROSE))):
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
    adapted = original
    for key, count in replacements.items():
        source = TYPED_SOURCE_KEYS[key]
        old = ('../../source-store/' + source.split('/source-store/', 1)[1]).encode()
        new = ('https://github.com/theislampill/orthemology/blob/' + TYPED_PROSE_REVISION + '/' + source).encode()
        if original.count(old) != count:
            raise ValueError('typed guide original link count differs')
        adapted = adapted.replace(old, new)
    current = _regular_current_bytes(root, path)
    if current != adapted and not (allow_original and current == original):
        raise ValueError('typed guide is not its exact navigation adaptation')
    adapted_blob = hashlib.sha1(b'blob ' + str(len(adapted)).encode() + b'\0' + adapted).hexdigest()
    indexed = git('ls-files', '--stage', '-z', '--', path)
    choices = {('100644 ' + oid + ' 0\t' + path + '\0').encode(): body
               for oid, body in ((blob, original), (adapted_blob, adapted))}
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
    return result


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
    return _checkpoint_bound_bytes(root, path, binding)


def checkpoint_duplicate_paths(root):
    """Return actual absences only after authenticating the complete finite class."""
    result = set()
    for path, binding in _checkpoint_copy_catalog().items():
        _checkpoint_bound_bytes(root, path, binding)
        if not os.path.lexists(pathlib.Path(root) / path):
            result.add(path)
    return result


def source_bytes(root, row):
    path = pathlib.PurePosixPath(row['repository_path'])
    if path.is_absolute() or '..' in path.parts or '\\' in str(path):
        raise ValueError('unsafe source path')
    if str(path) in HISTORICAL_PROSE:
        blob, identity, size = HISTORICAL_PROSE[str(path)]
        if (row['repository_path'] != str(path) or str(path) not in HISTORICAL_PROSE_PUBLIC_PATHS
                or row.get('disposition') != HISTORICAL_PROSE_DISPOSITIONS[str(path)]
                or row.get('source_sha256') != identity or row.get('source_bytes') != size):
            raise ValueError('historical public source owner differs')
        body = historical_source_bytes(root, str(path), row.get('repository_revision'), row.get('git_blob'))
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
