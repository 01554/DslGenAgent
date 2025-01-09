#!/usr/bin/env python3
"""

This product includes software originally developed by © 2024 LangGenius, Inc.
Modifications were made by HelloHazime on 2025.

Modifications:
 *  - 2025: CLIでymlのvalidationをできるようにservices.app_dsl_service にあった AppDslService をこちらにコピーして必須パラムを修正

-------------------
# Open Source License

Dify is licensed under the Apache License 2.0, with the following additional conditions:

1. Dify may be utilized commercially, including as a backend service for other applications or as an application development platform for enterprises. Should the conditions below be met, a commercial license must be obtained from the producer:

a. Multi-tenant service: Unless explicitly authorized by Dify in writing, you may not use the Dify source code to operate a multi-tenant environment. 
    - Tenant Definition: Within the context of Dify, one tenant corresponds to one workspace. The workspace provides a separated area for each tenant's data and configurations.
    
b. LOGO and copyright information: In the process of using Dify's frontend, you may not remove or modify the LOGO or copyright information in the Dify console or applications. This restriction is inapplicable to uses of Dify that do not involve its frontend.
    - Frontend Definition: For the purposes of this license, the "frontend" of Dify includes all components located in the `web/` directory when running Dify from the raw source code, or the "web" image when running Dify with Docker.

Please contact business@dify.ai by email to inquire about licensing matters.

2. As a contributor, you should agree that:

a. The producer can adjust the open-source agreement to be more strict or relaxed as deemed necessary.
b. Your contributed code may be used for commercial purposes, including but not limited to its cloud business operations.

Apart from the specific conditions mentioned above, all other rights and restrictions follow the Apache License 2.0. Detailed information about the Apache License 2.0 can be found at http://www.apache.org/licenses/LICENSE-2.0.

The interactive design of this product is protected by appearance patent.

© 2024 LangGenius, Inc.


----------

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


--------------------
以下の翻訳はDeepLによる自動翻訳です。
--------------------

DifyのライセンスはApache License 2.0です：

1. Difyは、他のアプリケーションのバックエンドサービスとして、または企業のアプリケーション開発プラットフォームとして、商業的に利用することができる。以下の条件を満たす場合は、製作者から商用ライセンスを取得する必要があります：

a. a. マルチテナントサービス： a. マルチテナントサービス：Difyが書面で明示的に許可しない限り、Difyのソースコードを使用してマルチテナント環境を運営することはできません。
    - テナントの定義： Dify では、1テナントは1ワークスペースに相当する。ワークスペースは、各テナントのデータと設定用に分離された領域を提供する。
    
b. ロゴと著作権情報 ：Difyのフロントエンドを使用する過程において、Difyコンソールまたはアプリケーションのロゴまたは著作権情報を削除または変更することはできません。この制限は、フロントエンドを伴わないDifyの使用には適用されません。
    - フロントエンドの定義 本ライセンスにおいて、Difyの「フロントエンド」には、生のソースコードからDifyを実行する場合は`web/`ディレクトリに、DockerでDifyを実行する場合は「web」イメージにあるすべてのコンポーネントが含まれます。

ライセンスに関するお問い合わせは、business@dify.ai までメールにてご連絡ください。

2. 2. 貢献者として、あなたは以下のことに同意する必要があります：

a. a.制作者は、必要と判断した場合、オープンソース契約をより厳しく、または緩和するように調整することができます。
b. あなたの貢献したコードは、そのクラウド事業運営を含むがこれに限定されない商業目的で使用することができる。

上記の特定の条件を除き、その他のすべての権利と制限はApacheライセンス2.0に従います。Apache License 2.0の詳細情報は、http://www.apache.org/licenses/LICENSE-2.0。

本製品のインタラクティブデザインは外観特許により保護されています。

© 2024 LangGenius, Inc.

--------------------
"""

import pprint
from typing import Optional
from pydantic import BaseModel
import yaml
from uuid import uuid4
from enum import StrEnum
from packaging import version


CURRENT_DSL_VERSION = "0.1.5"

class ImportMode(StrEnum):
    YAML_CONTENT = "yaml-content"
    YAML_URL = "yaml-url"


class ImportStatus(StrEnum):
    COMPLETED = "completed"
    COMPLETED_WITH_WARNINGS = "completed-with-warnings"
    PENDING = "pending"
    FAILED = "failed"


class Import(BaseModel):
    id: str
    status: ImportStatus
    app_id: Optional[str] = None
    current_dsl_version: str = CURRENT_DSL_VERSION
    imported_dsl_version: str = ""
    error: str = ""


def _check_version_compatibility(imported_version: str) -> ImportStatus:
    """Determine import status based on version comparison"""
    try:
        current_ver = version.parse(CURRENT_DSL_VERSION)
        imported_ver = version.parse(imported_version)
    except version.InvalidVersion:
        return ImportStatus.FAILED

    # Compare major version and minor version
    if current_ver.major != imported_ver.major or current_ver.minor != imported_ver.minor:
        return ImportStatus.PENDING

    if current_ver.micro != imported_ver.micro:
        return ImportStatus.COMPLETED_WITH_WARNINGS

    return ImportStatus.COMPLETED


class AppDslService:
    def import_app(
        self,
        import_mode: str,
        yaml_content: Optional[str] = None,
        yaml_url: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        icon_type: Optional[str] = None,
        icon: Optional[str] = None,
        icon_background: Optional[str] = None,
        app_id: Optional[str] = None,
    ) -> Import:
        """Import an app from YAML content or URL."""
        import_id = str(uuid4())

        # Validate import mode
        try:
            mode = ImportMode(import_mode)
        except ValueError:
            raise ValueError(f"Invalid import_mode: {import_mode}")

        # Get YAML content
        content = ""
        if not yaml_content:
            return Import(
                id=import_id,
                status=ImportStatus.FAILED,
                error="yaml_content is required when import_mode is yaml-content",
            )
        content = yaml_content

        # Process YAML content
        try:
            # Parse YAML to validate format
            data = yaml.safe_load(content)
            if not isinstance(data, dict):
                return Import(
                    id=import_id,
                    status=ImportStatus.FAILED,
                    error="Invalid YAML format: content must be a mapping",
                )

            # Validate and fix DSL version
            if not data.get("version"):
                data["version"] = "0.1.0"
            if not data.get("kind") or data.get("kind") != "app":
                data["kind"] = "app"

            imported_version = data.get("version", "0.1.0")
            status = _check_version_compatibility(imported_version)

            # Extract app data
            app_data = data.get("app")
            if not app_data:
                return Import(
                    id=import_id,
                    status=ImportStatus.FAILED,
                    error="Missing app data in YAML content",
                )


            

            return Import(
                id=import_id,
                status=status,
                app_id='appid',
                imported_dsl_version=imported_version,
            )

        except yaml.YAMLError as e:
            return Import(
                id=import_id,
                status=ImportStatus.FAILED,
                error=f"Invalid YAML format: {str(e)}",
            )

        except Exception as e:
            pprint.pprint(e)
            return Import(
                id=import_id,
                status=ImportStatus.FAILED,
                error=str(e),
            )





if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='Validate YML file')
    parser.add_argument('yml_path', type=str, help='Path to YML file to validate')
    args = parser.parse_args()

    try:
        import_service = AppDslService()
        with open(args.yml_path, 'r') as f:
            yaml_content = f.read()
        import_data = import_service.import_app(ImportMode.YAML_CONTENT.value, yaml_content)
        print( import_data.status )
        if import_data.status == ImportStatus.FAILED:
            print("YML file is invalid")
            print(import_data.error)
        elif import_data.status == ImportStatus.COMPLETED \
            or import_data.status == ImportStatus.COMPLETED_WITH_WARNINGS:
            # COMPLETED_WITH_WARNINGS はマイナーVer違いなので OKとする
            print("YML file is valid")
        else:
            print("YML file is invalid")

    except FileNotFoundError:
        print(f"Error: File not found at {args.yml_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
