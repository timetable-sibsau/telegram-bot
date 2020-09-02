import os
import asyncio

from config import PATH_TO_TT_FILES
from timetable_controller import get_timetable


async def update_timetables():
    files_names_fail_text = 'Что-то пошло не так при чтении имён файлов...'
    success_text = 'Всё сделано!'
    updating_process_fail = 'Проищошла ошибка при обновлении файлов...'
    try:
        # files_names = [".".join(f.split(".")[:-1]) for f in os.listdir(PATH_TO_TT_FILES) if os.path.isfile(f)]
        files = os.listdir(PATH_TO_TT_FILES)
        files_names = [file.split('.')[0] for file in files]
        # print(files_names)
        # return success_text
    except:
        return files_names_fail_text

    try:
        for file_name in files_names:
            await get_timetable(file_name)
        return success_text
    except:
        return updating_process_fail


if __name__ == '__main__':
    coroutine = update_timetables()
    print(asyncio.run(coroutine))
