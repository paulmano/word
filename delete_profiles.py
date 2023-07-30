import datetime
import os
import subprocess
import winreg


def delete_user_profiles():
    current_user = os.getlogin().casefold()
    log_info = []
    #log_file = open(f'C:\\Users\\{current_user}\\Documents\\logs.txt', 'a')

    exclude_folders = [current_user, 'Default', 'Public']
    excluded_folders = [folder.casefold() for folder in exclude_folders]
    users_folder = 'C:\\Users'

    # Folders in the Users folder
    user_folders = [folder.casefold() for folder in os.listdir(users_folder) if os.path.isdir(os.path.join(users_folder, folder))]

    log_info.append(f'User folders:: {user_folders} \n\n')

    # Folders to delete
    del_folders = [folder.casefold() for folder in user_folders if folder not in excluded_folders and not folder.startswith(('saf', 'sfc', current_user))]
    log_info.append(f'Folders to delete:: {del_folders} \n\n')

    # Delete the appropriate folders
    for folder in del_folders:
        folder_path = os.path.join(users_folder, folder).casefold()

        log_info.append(f'Folder paths to delete:: {folder_path} \n\n')

        try:
            subprocess.run(['rmdir', f'/s', f'/q', folder_path], shell=True)
            log_info.append(f'{datetime.datetime.now()}: Deleted user profiles: {del_folders} \n')

            # TODO:: Implement code to delete the user from the registry
            try:
                subkey = r'SOFTWARE\\Microsoft\Windows NT\\CurrentVersion\\ProfileList'
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey) as key:  # Open profile list
                    user_sid = winreg.QueryInfoKey(key)[0]  # The total number of subkeys [profiles in the ProfileList]
                    log_info.append(f'Number of profiles:: {user_sid} \n')

                    for i in range(user_sid):
                        sid = winreg.EnumKey(key, i)

                        log_info.append(f'SID:: {sid} \n')  # sid is a subkey of key [a single profile in a profile list]

                        try:
                            with winreg.OpenKey(key, sid) as user_key:  # Open a single profile
                                profile_path = winreg.QueryValueEx(user_key, 'ProfileImagePath')[0].casefold()  # user profile path e.g C:/Users/Mano

                                log_info.append(f'Folder path:: {folder_path} Profile path:: {profile_path} \n')

                                if folder_path == profile_path:
                                    log_info.append(f'Folder path {folder_path} equals profile path {profile_path} :: and its key:: {sid} should be deleted \n')

                                    winreg.DeleteKey(key, sid)
                                    log_info.append(f"Deleted user profile registry key: {sid} \n")

                                    #break
                        except Exception as e:
                            log_info.append(f'Error occurred while deleting user profile registry key: {e} \n')

            except Exception as e:
                log_info.append(f'Error occurred while deleting user profile registry key: {e} \n')
            # End TODO::
            
        except Exception as e:
            log_info.append(f'Error occurred while deleting profiles: {del_folders}: {e} \n')



        with open(f'C:\\Users\\{current_user}\\Documents\\logs.txt', 'a') as log_file:
            log_file.writelines(log_info)


if __name__ == '__main__':
    delete_user_profiles()
