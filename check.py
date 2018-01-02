# __*__ coding:utf-8 __*__
__author__ = 'Chale'
__date__ = '2017/12/27 9:27'
__describe__ = u'检查索引文件与实际数据文件的一致性，需满足索引文件中的文件名与实际文件文件名一致'
__email__ = 'funcgis@163.com'

import sys
import getopt
import os


def list_index(index):
    print u"正在扫描索引文件..."
    f = open(index)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    lines = []
    if line is not None and line != "":
        lines.append(line.replace("\n", ""))
    while line:
        line = f.readline()
        if line is not None and line != "":
            lines.append(line.replace("\n", ""))
    return lines


def get_linetext(line, startnum, endnum):
    linestr = line.replace("\n", "")
    ifLenFine = False #判断截取长度是否在字符长度范围内，否侧不截取
    if startnum > len(linestr) or endnum > len(linestr):
        print u'截取索引超出字符串长度！跳过截取操作'
        startnum = 0
        endnum = len(linestr)
    if endnum == 0:
        linestr = linestr[startnum: len(linestr)]
    else:
        linestr = linestr[startnum: endnum]
    return linestr


def list_indexsub(index, startnum, endnum):
    print u"正在扫描索引文件..."
    f = open(index)
    line = f.readline()
    lines = []
    if line is not None and line != "":
        lines.append(get_linetext(line, startnum, endnum))
    while line:
        line = f.readline()
        if line is not None and line != "":
            lines.append(get_linetext(line, startnum, endnum))
    return lines


def list_folder(folder):
    print u"正在扫描目录..."
    listfiles = []
    for root, dirs, files in os.walk(folder):
        listfiles = files
    return listfiles


def save_list(listData, savePath):
    print u'正在输出到：', savePath
    file = open(savePath, 'w')
    for i in listData:
        file.write(str(i) + '\n')
    file.close()


def check(index, folder, out, ifout, ifright, ifsubindex, startnum, endnum):
    lines = files = None
    if os.path.exists(index):
        if ifsubindex:
            lines = list_indexsub(index, startnum, endnum)
        else:
            lines = list_index(index)
    else:
        print u'输入索引文件不存在！'
    if os.path.exists(folder):
        files = list_folder(folder)
    else:
        print u'输入文件夹不存在！'

    listlines = listfiles = []
    if lines is not None and len(lines) >= 0:
        if files is not None and len(files) >= 0:
            listlines = list(set(lines).difference(set(files)))
            print u'未含索引文件', listlines
            if ifright:
                listfiles = list(set(files).difference(set(lines)))
                print u'未含目录文件', listfiles
            if ifout:
                if len(listlines) > 0 or len(listfiles) > 0:
                    if out is not None and out != "":
                        if os.path.exists(out) and len(listlines) > 0:
                            save_list(listlines, out + '\\inIndexNotInFolder.txt')
                        if len(listfiles) > 0:
                            save_list(listfiles, out + '\\inFolderNotInIndex.txt')
                    else:
                        if len(listlines) > 0:
                            save_list(listlines, os.getcwd() + '\\inIndexNotInFolder.txt')
                        if len(listfiles) > 0:
                            save_list(listfiles, os.getcwd() + '\\inFolderNotInIndex.txt')
                else:
                    print u'索引文件与文件夹内文件一致！，没有输出差异文件。'
        else:
            print u'文件夹为空！'
    else:
        print u'索引文件为空！'


def get_help():
    print u"作者：", __author__, '\n', u"编写日期：", __date__, '\n', \
        u"描述：", __describe__, '\n', u"联系方式：", __email__
    print '\n', u"使用方式：", '\n', u"-i         输入索引文件", '\n', u"-f         输入实际文件文件夹", '\n'\
        u"-k         是否输出结果文件（可选）", \
        '\n', u"-o         与 -k 一起使用，指定输出文件路径，默认为程序执行当前路径（可选）",\
        '\n', u"-r         是否反向对比（即文件夹中存在，索引文件中不存在）（可选）", \
        '\n', u"-c         是否截取索引记录字符串子串进行对比（可选）", \
        '\n', u"-s         否截取索引记录字符串子串起始字符数（可选，-c启用时生效，默认为0）", \
        '\n', u"-e         否截取索引记录字符串子串终止字符数（可选，-c启用时生效，默认为全长）", \
        '\n', u"-h         查看帮助"
    print '\n', u"使用示例：", '\n', u"python ./check.py -i index.txt -f E:\\test -o E:\\test -c -s 1 -e 56"


def get_error():
    print u"请输入 -i, -f 两个必须参数，详细请输入 -h 查看帮助"


def main(argv):
    indexfile = u""
    foldername = u""
    outfile = u""
    ifout = False
    ifright = False
    ifsubindex = False
    startnum = 0
    endnum = 0

    try:
        opts, args = getopt.getopt(argv, "hkrci:f:o:s:e:", ["indexfile=", "foldername=", "outfile="])
    except getopt.GetoptError:
        get_error()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            get_help()
            sys.exit()
        elif opt in ("-i", "--indexfile"):
            indexfile = arg
        elif opt in ("-f", "--foldername"):
            foldername = arg
        elif opt in ("-o", "--outfile"):
            outfile = arg
        elif opt in ("-r", "--ifright"):
            ifright = True
        elif opt in ("-k", "--ifout"):
            ifout = True
        elif opt in ("-c", "--ifsubindex"):
            ifsubindex = True
        elif opt in ("-s", "--startnum"):
            startnum = int(arg)
        elif opt in ("-e", "--endnum"):
            endnum = int(arg)

    if indexfile != "" and foldername != "":
        check(indexfile, foldername, outfile, ifout, ifright, ifsubindex, startnum, endnum)
    else:
        get_error()


if __name__ == "__main__":
    main(sys.argv[1:])

