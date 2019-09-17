#!/usr/bin/python
import os,sys,re

def search_values_in_file(argv):
    source_file=argv[1];
    dest_file=argv[2];
    if os.path.exists(source_file)==False:
        print "err source file"
        exit(0)
    elif os.path.exists(dest_file)==False:
        print "err dest file"
        exit(0)
    source_path_list = get_flie_list(source_file);
    dest_path_list = get_flie_list(dest_file);
    source_string_list_map = get_attr_name_map(source_path_list);
    replace_dest_file_content(dest_path_list, source_string_list_map);

def get_flie_list(path_file):
    list = os.listdir(path_file);
    source_path_list=[];
    for i in range(0, len(list)):
        path = os.path.join(path_file, list[i]);
        if os.path.isfile(path):
            source_path_list.append(path);
    return source_path_list;

def get_attr_name_map(list):
    string_name_list = [];
    map = {};
    for path in list:
        f = open(path, "r");
        lines = f.readlines();
        temp_name='';
        for line in lines:
            if line.find("<string ") < 0:
                if temp_name != '':
                    map[temp_name] = map[temp_name] + line;
                continue;
            temp_name='';
            pattern = re.compile('(?<=\")[^\"]+(?=\")', re.I);
            string_name = pattern.findall(line)[0];
            string_name_list.append(string_name);
            if line.find("</string>") < 0:
                temp_name = string_name;
            map[string_name] = line;
    return map;

def replace_dest_file_content(dest_path, map):
    #print "dest_path:%s, map:%s" % (dest_path, map.keys());
    cout = 0;
    for path in dest_path:
        # if cout==4:
        #     break;
        # cout+=1;
        # if path != '/work/hm-master/vendor/huami/packages/Experimental/NewSport/app/src/main/res/values-ru/elliptical_strings.xml' :
        #     continue;
        s = [];
        f = open(path, "r");
        lines = f.readlines();
        is_multi_line = False;
        for line in lines:
            if line.find("<string ") < 0:
                if is_multi_line == False:
                    s.append(line);
                if line.find("</string>") > 0:
                    is_multi_line = False;
                continue;
            if line.find("</string>") < 0:
                is_multi_line = True;
            else:
                is_multi_line = False;

            pattern = re.compile('(?<=\")[^\"]+(?=\")', re.I);
            string_name = pattern.findall(line)[0];
            for key in map.keys():
                if key == string_name:
                    print("corres key:", key);
                    line = map[key];
            s.append(line);
        print("s", s);
        #s = ''.join(lines);
        #print("content:", s);
        f.close();
        f = open(path, 'r+b');
        content='';
        for line in s:
            content = content + line;
        f.truncate();
        f.write(content);
        f.close();
            

if __name__=="__main__":
    if (sys.argv) < 3:
        print "it must be more than two params"
        exit(0)
    #test_re();
    search_values_in_file(sys.argv)