import requests
import json
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = 'y0__wgBELzBv5wFGNuWAyCoy-HSGTCg8IatCK5mrWdvMRrChI7BBPoOsptk9JFB'
FOLDER_NAME = 'aiepyapi-162'


def get_cat_image(text):
    url = f'https://cataas.com/cat/cute/says/{text}'

    try:

        response = requests.get(url, timeout=10, verify=False)

        if response.status_code == 200:
            return response.content
        else:
            print(f'Ошибка при получении картинки: {response.status_code}')
            return None
    except Exception as e:
        print(f'Ошибка сети: {e}')
        return None


def create_folder_on_disk(folder_name):
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {'Authorization': f'OAuth {TOKEN}'}
    params = {'path': folder_name}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10, verify=False)
        if response.status_code == 404:
            response = requests.put(url, headers=headers, params=params, timeout=10, verify=False)
            if response.status_code == 201:
                print(f'Папка {folder_name} успешно создана.')
            else:
                print(f'Ошибка создания папки: {response.status_code}')
        elif response.status_code == 200:
            print(f'Папка {folder_name} уже существует.')
    except Exception as e:
        print(f'Ошибка сети при создании папки: {e}')


def upload_to_yandex_disk(file_path, disk_filename):
    upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = {'Authorization': f'OAuth {TOKEN}'}
    params = {'path': disk_filename, 'overwrite': 'true'}

    try:
        response = requests.get(upload_url, headers=headers, params=params, timeout=10, verify=False)
        if response.status_code != 200:
            print(f'Ошибка запроса на загрузку: {response.text}')
            return False

        upload_href = response.json()['href']

        with open(file_path, 'rb') as f:
            upload_response = requests.put(upload_href, files={'file': f}, timeout=30, verify=False)

        if upload_response.status_code == 201:
            print(f'Файл {disk_filename} успешно загружен!')
            return True
        else:
            print(f'Ошибка загрузки файла: {upload_response.status_code}')
            return False
    except Exception as e:
        print(f'Ошибка сети при загрузке: {e}')
        return False


if __name__ == '__main__':
    text = 'Python'
    print('Скачиваем котика...')
    image_data = get_cat_image(text)

    if image_data:
        create_folder_on_disk(FOLDER_NAME)

        local_filename = 'test_cat.jpg'
        with open(local_filename, 'wb') as f:
            f.write(image_data)

        disk_filename = f'{FOLDER_NAME}/{text}.jpg'
        upload_to_yandex_disk(local_filename, disk_filename)

        if os.path.exists(local_filename):
            os.remove(local_filename)
            print('Локальный файл удален.')

        print("Запрашиваем информацию о файле...")
        info_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Authorization': f'OAuth {TOKEN}'}
        params = {'path': disk_filename}

        try:
            info_response = requests.get(info_url, headers=headers, params=params, timeout=10, verify=False)
            if info_response.status_code == 200:
                file_info = info_response.json()
                file_size = file_info.get('size')

                result_data = {
                    "filename": disk_filename,
                    "size": file_size
                }

                with open('result.json', 'w', encoding='utf-8') as f:
                    json.dump(result_data, f, ensure_ascii=False, indent=4)

                print(f"Информация сохранена в result.json (Размер: {file_size} байт)")
            else:
                print(f"Не удалось получить информацию: {info_response.status_code}")
        except Exception as e:
            print(f"Ошибка при получении размера: {e}")
