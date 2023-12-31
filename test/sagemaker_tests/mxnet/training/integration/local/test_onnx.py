# Copyright 2018-2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
from __future__ import absolute_import

import os

import pytest

from sagemaker.mxnet import MXNet

from ...integration.local import local_mode_utils
from ...integration import RESOURCE_PATH

ONNX_PATH = os.path.join(RESOURCE_PATH, "onnx")
SCRIPT_PATH = os.path.join(ONNX_PATH, "code", "onnx_export.py")


@pytest.mark.integration("onnx")
@pytest.mark.model("onnx_model")
def test_onnx_export(
    docker_image, sagemaker_local_session, local_instance_type, framework_version, tmpdir
):
    mx = MXNet(
        entry_point=SCRIPT_PATH,
        role="SageMakerRole",
        instance_count=1,
        instance_type=local_instance_type,
        sagemaker_session=sagemaker_local_session,
        image_uri=docker_image,
        framework_version=framework_version,
        output_path="file://{}".format(tmpdir),
    )

    mx.fit()

    local_mode_utils.assert_output_files_exist(str(tmpdir), "output", ["success"])
