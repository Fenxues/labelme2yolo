import os, shutil
import glob
import json
import argparse
def handle_dir(path):
    ## if not exists, then creat it
    if not os.path.isdir(path):
        os.makedirs(path)
    elif not os.listdir(path):
        pass
    else:
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            os.remove(file_path)
    print("the directory has been handled.")
    return

def count_files_with_extension(folder_path, extension):
    pattern = f"{folder_path}/*{extension}"
    file_list = glob.glob(pattern, recursive=True)
    return len(file_list)

def make_yolo_dataset(data_dir, val_ratio, target_dir):
    num_data = count_files_with_extension(data_dir, '.json')
    num_val_data = int(num_data * val_ratio)
    num_train_data = num_data - num_val_data
    ### check path exists or not
    handle_dir(target_dir + '/labels/train')
    handle_dir(target_dir + '/labels/val')
    handle_dir(target_dir + '/images/train')
    handle_dir(target_dir + '/images/val')
    cnt = 1
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            if cnt <= num_train_data:
                shutil.copyfile(os.path.join(data_dir, filename.split('.')[0] + '.txt'), target_dir + '/labels/train/' + str(cnt) + '.txt')
                shutil.copyfile(os.path.join(data_dir, filename.split('.')[0] + '.png'), target_dir + '/images/train/' + str(cnt) + '.png')
            else:
                shutil.copyfile(os.path.join(data_dir, filename.split('.')[0] + '.txt'), target_dir + '/labels/val/' + str(cnt) + '.txt')
                shutil.copyfile(os.path.join(data_dir, filename.split('.')[0] + '.png'), target_dir + '/images/val/' + str(cnt) + '.png')

            cnt += 1
    print("数据集已制作完毕.")
    return

def json2yolo(directory_path, label_style,pose_list):
    # 确保路径存在
    if not os.path.exists(directory_path):
        print(f"指定的路径 '{directory_path}' 不存在")
        return

    # 遍历目录中的所有文件
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        nam_ind = filename.split(".")[0]

        # 检查文件是否是JSON文件
        if filename.endswith('.json'):
            # 打开并读取JSON文件
            with open(filepath, 'r', encoding='utf-8') as file:
                try:
                    # 解析JSON数据
                    jd = json.load(file)
                    height = jd['imageHeight']
                    width = jd['imageWidth']
                    jds = jd['shapes']  ##jds:list of dicts
                    num_jds = len(jds)
                    # print("total objects: ", int(num_jds/3))
                    num_rec = int(num_jds / 3)
                    #print(num_rec)
                    with open(directory_path + '/' + nam_ind + ".txt", 'w') as file_handle:
                        for i in range(0, num_rec):
                            if label_style == "group":
                                for idx, var_name in enumerate(pose_list):
                                    print(pose_list)
                                    exec(var_name+' = '+'jds[num_rec*'+str(idx)+'+'+str(i)+']')
                            elif label_style == "single":
                                for idx, var_name in enumerate(pose_list):
                                    exec(var_name+' = '+'jds['+str(i)+'*'+str(len(pose_list))+'+'+str(idx)+']')
                                # group
                                #fish = jds[i]
                                #fish_head = jds[num_rec * 1 + i]
                                #fish_body = jds[num_rec * 2 + i]

                                # single
                                # fish = jds[i*3]
                                # fish_head = jds[i*3+1]
                                # fish_body = jds[i*3+ 2]
                            # x_center = 0
                            # y_center = 0
                            # w = 0
                            # h = 0
                            exec('x_center = round(('+pose_list[0]+r"['points'][1][0] + "+pose_list[0]+r"['points'][0][0]) / (2 * width), 3)")
                            exec('y_center = round(('+pose_list[0]+r"['points'][1][1] + "+pose_list[0]+r"['points'][0][1]) / (2 * height), 3)")
                            exec('w = round(('+pose_list[0] + r"['points'][1][0] - " + pose_list[0] + r"['points'][0][0]) / (1 * width), 3)")
                            exec('h = round((' + pose_list[0] + r"['points'][1][1] - " + pose_list[0] + r"['points'][0][1]) / (1 * height), 3)")
                            #x_center = round((fish['points'][1][0] + fish['points'][0][0]) / (2 * width), 3)
                            #y_center = round((fish['points'][1][1] + fish['points'][0][1]) / (2 * height), 3)
                            #w = round((fish['points'][1][0] - fish['points'][0][0]) / (1 * width), 3)
                            #h = round((fish['points'][1][1] - fish['points'][0][1]) / (1 * height), 3)
                            # .txt可以不自己新建,代码会自动新建
                            file_handle.write(str(0))  # class ?
                            file_handle.write(" ")
                            exec('file_handle.write(str(x_center))')
                            file_handle.write(" ")
                            exec('file_handle.write(str(y_center))')
                            file_handle.write(" ")
                            exec('file_handle.write(str(w))')
                            file_handle.write(" ")
                            exec('file_handle.write(str(h))')
                            file_handle.write(" ")
                            for i in range(1,len(pose_list)):
                                exec('file_handle.write(str(round('+pose_list[i]+r"['points'][0][0] / width, 3)))")
                                file_handle.write(" ")
                                exec('file_handle.write(str(round(' + pose_list[i] + r"['points'][0][1] / height, 3)))")
                                file_handle.write(" ")
                            file_handle.write('\n')
                            #file_handle.write(str(round(fish_head['points'][0][0] / width, 3)))
                            #file_handle.write(" ")
                            #file_handle.write(str(round(fish_head['points'][0][1] / height, 3)))
                            #file_handle.write(" ")
                            #file_handle.write(str(round(fish_body['points'][0][0] / width, 3)))
                            #file_handle.write(" ")
                            #file_handle.write(str(round(fish_body['points'][0][1] / height, 3)))
                            #file_handle.write(" ")
                            #file_handle.write('\n')
                            # print(fish_head)
                    # print(jd['shapes'])

                except json.JSONDecodeError as e:
                    print(f"解析JSON文件 '{filename}' 时出错: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument("--pose_list", nargs='+',type=str, required=True)
    parser.add_argument("--data_dir", type = str)
    parser.add_argument("--label_style",type = str, default="single")
    parser.add_argument("--val_ratio", type = float, default=0.2)
    parser.add_argument("--target_dir",type=str)
    args = parser.parse_args()
    # json2yolo(directory_path="D:/test",label_style='group',pose_list =
    #           ['fish','fish_head','fish_body'])
    # make_yolo_dataset(data_dir="D:/test",val_ratio=0.2,target_dir="D:/test/project")
    json2yolo(directory_path=args.data_dir,label_style=args.label_style,pose_list =
              args.pose_list)
    make_yolo_dataset(data_dir=args.data_dir,val_ratio=args.val_ratio,target_dir=args.target_dir)


