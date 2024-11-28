import os, shutil
import glob
import argparse

def count_files_with_extension(folder_path, extension):
    pattern = f"{folder_path}/*{extension}"
    file_list = glob.glob(pattern, recursive=True)
    return len(file_list)

def merge_jsons(path_1, path_2, obj_path):
    """
    merge two data folders with label-me format
    """
    if not os.path.exists(obj_path):
        os.mkdir(obj_path)
        print("目标文件夹为空，现已创建")

    if not os.path.exists(path_1):
        print("源文件夹: "+path_1+" 为空，请使用正确的数据来源")
        return

    if not os.path.exists(path_2):
        print("源文件夹: "+path_2+" 为空，请使用正确的数据来源")
        return

    if len(os.listdir(path_1)) == 0 or len(os.listdir(path_2)) == 0:
        print("源文件夹为空，请使用正确的数据来源")

        return
    if path_1 == obj_path:
        len_obj = count_files_with_extension(path_1, '.json')
        cnt = 1
        for filename in os.listdir(path_2):
            if filename.endswith('.json'):
                new_name = str(cnt + len_obj) + '.json'
                shutil.copyfile(os.path.join(path_2, filename), os.path.join(obj_path, new_name))
                new_name_png = str(cnt + len_obj) + '.png'
                shutil.copyfile(os.path.join(path_2, filename.split('.')[0] + '.png'),
                                os.path.join(obj_path, new_name_png))
                cnt += 1
        print("已将路径:"+path_1+"和路径:"+path_2+"下的数据合并到了路径:"+obj_path)

    elif path_2 == obj_path:
        len_obj = count_files_with_extension(path_2, '.json')
        cnt = 1
        for filename in os.listdir(path_1):
            if filename.endswith('.json'):
                new_name = str(cnt + len_obj) + '.json'
                shutil.copyfile(os.path.join(path_1, filename), os.path.join(obj_path, new_name))
                new_name_png = str(cnt + len_obj) + '.png'
                shutil.copyfile(os.path.join(path_1, filename.split('.')[0] + '.png'),
                                os.path.join(obj_path, new_name_png))
                cnt += 1
        print("已将路径:"+path_1+"和路径:"+path_2+"下的数据合并到了路径:"+obj_path)
    else:
        cnt = 1
        for filename in os.listdir(path_1):
            if filename.endswith('.json'):
                new_name = str(cnt) + '.json'
                shutil.copyfile(os.path.join(path_1, filename), os.path.join(obj_path, new_name))
                new_name_png = str(cnt) + '.png'
                shutil.copyfile(os.path.join(path_1, filename.split('.')[0] + '.png'),
                                os.path.join(obj_path, new_name_png))
                cnt += 1
        for filename in os.listdir(path_2):
            if filename.endswith('.json'):
                new_name = str(cnt) + '.json'
                shutil.copyfile(os.path.join(path_2, filename), os.path.join(obj_path, new_name))
                new_name_png = str(cnt) + '.png'
                shutil.copyfile(os.path.join(path_2, filename.split('.')[0] + '.png'),
                                os.path.join(obj_path, new_name_png))
                cnt += 1
        print("已将路径:"+path_1+"和路径:"+path_2+"下的数据合并到了路径:"+obj_path)

if __name__ =="__main__":
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument("--path1", type=str)
    parser.add_argument("--path2", type=str)
    parser.add_argument("--obj_path", type=str)
    args = parser.parse_args()
    merge_jsons(args.path1, args.path2, args.obj_path)

