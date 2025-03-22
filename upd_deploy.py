#
# Copyright (C) 2024 CrowdWare
#
# This file is part of NoCodeDesigner.
#
#  NoCodeDesigner is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  NoCodeDesigner is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with NoCodeDesigner.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import re
from datetime import datetime

"""Add file entries to the deployment descriptor."""

def update_deployment(app_sml_path, deployment_data):
    with open(app_sml_path, 'r') as file:
        app_sml_content = file.read()

    # Check if the file ends with a closing brace and remove it temporarily
    ends_with_brace = app_sml_content.rstrip().endswith('}')
    if ends_with_brace:
        app_sml_content = app_sml_content.rstrip()[:-1].rstrip()  # Remove the final brace

    # Match the deployment section and ensure it starts and ends correctly
    deployment_section_regex = re.compile(r"// deployment start.*?// deployment end", re.DOTALL)

    # Create the deployment block content
    deployment_block = f"""// deployment start - don't edit here
Deployment {{
{deployment_data}
}}
// deployment end"""

    # Replace or add the deployment block
    if deployment_section_regex.search(app_sml_content):
        # Replace existing deployment section
        app_sml_content = deployment_section_regex.sub(deployment_block, app_sml_content)
    else:
        # Append if not found
        app_sml_content = app_sml_content + '\n' + deployment_block

    # Re-add the final brace if it was there initially
    if ends_with_brace:
        app_sml_content += '\n}'

    # Write back the modified content
    with open(app_sml_path, 'w') as file:
        file.write(app_sml_content)


"""Generate a list of files and their last modified date for deployment data."""
def generate_deployment_data(type, base_path, exclude_files=None):
    if exclude_files is None:
        exclude_files = []

    deployment_entries = []
    for dirpath, _, filenames in os.walk(base_path):
        for filename in filenames:
            if filename not in exclude_files and not filename.startswith('.'):
                file_path = os.path.relpath(os.path.join(dirpath, filename), base_path)
                mod_time = os.path.getmtime(os.path.join(dirpath, filename))
                formatted_time = datetime.utcfromtimestamp(mod_time).strftime('%Y.%m.%d %H.%M.%S')
                # Append each entry in the correct format
                deployment_entries.append(f'  File {{ path: "{file_path}" time: "{formatted_time}" type: "{type}" }}')

    # Return formatted entries as a single string
    return "\n".join(deployment_entries)


def update():
    base_path = os.getcwd()
    app_sml_path = os.path.join(base_path, 'app.sml')

    # Paths for various types of deployment data
    paths = {
        "page": os.path.join(base_path, 'pages'),
        "part": os.path.join(base_path, 'parts'),
        "image": os.path.join(base_path, 'images'),
        "sound": os.path.join(base_path, 'sounds'),
        "video": os.path.join(base_path, 'videos'),
        "texture": os.path.join(base_path, 'textures'),
        "model": os.path.join(base_path, 'models'),
    }

    # Collect deployment data for all paths and types
    deployment_data = ""
    for data_type, path in paths.items():
        deployment_data += generate_deployment_data(data_type, path, exclude_files=['.DS_Store']) + "\n"

    print("Updating app.sml with deployment files...")
    update_deployment(app_sml_path, deployment_data.strip())


if __name__ == "__main__":
    update()