import sys
sys.path.append(".")

def str2float(item):
    if 'e' not in item:
        return float(item)
    itemVec = item.split('e')
    num = float(itemVec[0])
    exp = 1
    if itemVec[1][0] == '+':
        exp = 10 ** int(itemVec[1][1:])
    else:
        exp = 0.1 ** int(itemVec[1][1:])

    return num * exp


if __name__ == "__main__": 
    
    # insert your files here
    fileList = ["./static/basechannel114_res.csv","./static/andlutchannel114_res.csv","./static/andanddlutRvpr114_res.csv", "./static/base_res_lut7_114.csv"]
    # insert your baseline here
    fileBase = "./static/basechannel114_res.csv"
    # insert your carelist // ignore this if empty
    careFiles = ""
    # careFiles = "LU32PEEng.odin.blif  arm_core.odin.blif  blob_merge.odin.blif  mcml.odin.blif              mkPktMerge.odin.blif     or1200.odin.blif     sha.odin.blif    stereovision0.odin.blif  stereovision2.odin.blif \
    #         LU8PEEng.odin.blif   bgm.odin.blif       boundtop.odin.blif    mkDelayWorker32B.odin.blif  mkSMAdapter4B.odin.blif  raygentop.odin.blif  spree.odin.blif  stereovision1.odin.blif  stereovision3.odin.blif"
    
    
    lineVec = careFiles.split()
    carelist = []
    for file in lineVec:
        carelist.append(file[:-10])

    results = []
    params = []
    names = []
    names.append("__avg__")
    with open(fileList[0], 'r') as fi:
        bench = {}
        line = fi.readline()
        lineVec = line.replace('\n','').replace(' ','').split(",")
        for item in lineVec[1:]:
            params.append(item)
        while line:
            line = fi.readline()
            if len(line) == 0:
                continue
            lineVec = line.replace('\n','').replace(' ','').split(",")
            if len(carelist) > 0 and lineVec[0][:-5] not in carelist:
                print("MESSAGE: " + lineVec[0][:-5] + " of " + fileList[0] + " not in carelist, ignored")
                continue
            bench[lineVec[0][:-5]]={}
            names.append(lineVec[0][:-5])
            if len(params) != len(lineVec)-1:
                print("ERROR: " + lineVec[0] + " in " + fileList[0] + " length error")
            for idy in range(1, len(lineVec)):
                bench[lineVec[0][:-5]][params[idy-1]] = str2float(lineVec[idy])
        results.append(bench)
    

    for file in fileList:
        if file == fileBase:
            continue
        with open(file, 'r') as fi:
            bench = {}
            thisparams = []
            line = fi.readline()
            lineVec = line.replace('\n','').replace(' ','').split(",")
            for item in lineVec[1:]:
                thisparams.append(item)
            while line:
                line = fi.readline()
                if len(line) == 0:
                    continue
                lineVec = line.replace('\n','').replace(' ','').split(",")
                if lineVec[0] not in names:
                    print("MESSAGE: " + lineVec[0] + " of " + file + " not in baseline, ignored")
                    continue
                bench[lineVec[0]]={}
                for idy in range(1, len(lineVec)):
                    bench[lineVec[0]][thisparams[idy-1]] = str2float(lineVec[idy])
        results.append(bench)

    data = []

    for idx in range(1, len(results)):
        benchdata = {}
        parsum = [0.0] * len(params)
        parnum = [0] * len(params)
        for bench in results[idx]:
            benchdata[bench] = []
            for idy in range(0, len(params)):
                param = params[idy]
                if param not in results[idx][bench] or param not in results[0][bench] \
                   or results[idx][bench][param] == 0 or results[0][bench][param] == 0:
                    benchdata[bench].append(-2.0)
                else:
                    deviation = results[idx][bench][param] / results[0][bench][param] - 1
                    benchdata[bench].append(deviation)
                    parnum[idy]+=1
                    parsum[idy]+=deviation
            benchdata["__avg__"] = []
            for idy in range(0, len(params)):
                    if parnum[idy] == 0:
                        benchdata["__avg__"].append(-2.0)
                    else:
                        benchdata["__avg__"].append(parsum[idy]/parnum[idy])
        data.append(benchdata)

    print()
    for param in params:
        print(param,end=" ")
    print()
    for idx in range(0, len(data)):
        print("=============  "+fileList[1+idx]+"  ============")
        for name in names:
            if name not in data[idx]:
                continue
            print(name,end=" : ")
            print(' ' * (30 - len(name)),end="")
            for idy in range(0, len(params)):
                if(data[idx][name][idy] == -2.0):
                    print("null",end=", ")
                else:
                    print(round(data[idx][name][idy] * 100, 1),end=", ")
            print()
        print()