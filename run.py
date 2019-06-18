"""
Copyright (c) 2018 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

from controllers.ucsmcontroller import UCSMController
from controllers import imcsupcontroller
import traceback

if __name__ == "__main__":
    """******* vNIC profiles *******"""

    # Get interface profiles from UCS-M

    oUCSMController = UCSMController()
    try:

        print("\n\n======= BIOS Policies =======")

        biosProfiles = oUCSMController.GetBIOSProfiles()
        for profile in biosProfiles:
            profileDetails = oUCSMController.GetByDN(dn=profile.dn)
            biosPolicy = {"name": profile.name}
            for detail in profileDetails:
                if detail.dn.endswith("POST-error-pause"):
                    biosPolicy["POST-error-pause"] = detail.vp_post_error_pause
                    break

            # Create BIOS policy in IMC Sup
            imcsupcontroller.CreateBIOSPolicy(biosPolicy)

        print("\n\n======= VIC Policies =======")
        svcProfiles = oUCSMController.GetSvcProfiles()
        for svcProfile in svcProfiles:
            # Networking variables
            vicAdapterPolicy = {"name": svcProfile.name + "-vic"}
            vicAdapterPolicy["vNICs"] = []
            vicAdapterPolicy["vHBAs"] = []
            # Get the service profile details
            svcProfileDetail = oUCSMController.GetByDN(dn=svcProfile.dn)
            for item in svcProfileDetail:
                # Check networking
                if item._class_id == "VnicEther":
                    # Found eth interface
                    vicAdapterPolicy["vNICs"].append({"name": item.name, "mtu": item.mtu})
                elif item._class_id == "VnicFc":
                    # Found fiber channel
                    vicAdapterPolicy["vHBAs"].append({"name": item.name})

            # Created vic profile in IMC Supervisor
            imcsupcontroller.CreateVICAdapterPolicy(vicAdapterPolicy)


    except Exception as e:
        print(traceback.print_exc())
        print(str(e))
    finally:
        oUCSMController.Logout()
