import json
import copy

class Organizer:
    def __init__(self, final_kaplas: list):
        self.final_kaplas: list = final_kaplas

    def get_sequence(self):
        with open('resources/construction.json') as json_data:
            data = json.load(json_data)
            kapla_list = copy.deepcopy(data)

        list_size = len(kapla_list)
        Zmin = 99999
        prio_mini = 4
        suppr = 0
        prio = []
        data_tri = []
        pos = []
        ang = []
        face = []

        dic_ang = {}
        dic_ang[(20, 25, 70)] = 0
        dic_ang[(25, 20, 70)] = 90
        dic_ang[(20, 70, 25)] = 0
        dic_ang[(70, 20, 25)] = 90
        dic_ang[(25, 70, 20)] = 0
        dic_ang[(70, 25, 20)] = 90

        dic_face = {}
        dic_face[70] = 'small_face'
        dic_face[25] = 'medium_face'
        dic_face[20] = 'big_face'

        for i in range(len(kapla_list)):
            if kapla_list[i]["attitude"][2] == 20:
                prio.append(0)
            elif kapla_list[i]["attitude"][2] == 25:
                prio.append(1)
            elif kapla_list[i]["attitude"][2] == 70:
                prio.append(2)

        for i in range(list_size):
            for y in range(len(kapla_list)):
                if Zmin > kapla_list[y]["base"][2]:
                    Zmin = kapla_list[y]["base"][2]
            for y in range(len(kapla_list)):
                if kapla_list[y]["base"][2] == Zmin and prio_mini > prio[y]:
                    prio_mini = prio[y]
                    suppr = y
            Zmin = 99999
            prio_mini = 4
            data_tri.append(kapla_list[suppr])
            del kapla_list[suppr]

        for i in range(len(data_tri)):

            ang_1 = data_tri[i]["attitude"][0]
            ang_2 = data_tri[i]["attitude"][1]
            ang_3 = data_tri[i]["attitude"][2]
            ang.append(dic_ang[(ang_1,ang_2,ang_3)] + data_tri[i]["pivot"])

            pos_x = ( data_tri[i]["base"][0] + ( data_tri[i]["attitude"][0]/2 ))
            pos_y = ( data_tri[i]["base"][1] + ( data_tri[i]["attitude"][1]/2 ))
            pos_z = ( data_tri[i]["base"][2] + ( data_tri[i]["attitude"][2]/2 ))
            pos.append((pos_x, pos_y, pos_z))

            face.append(dic_face[data_tri[i]["attitude"][2]])

        while(1):
            for i in range(len(data)):
                yield (pos[i], ang[i], face[i])
            pass