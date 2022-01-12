from kivy.app import App
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from collections import Counter


class FamilyTreeCanvas(RelativeLayout):

    def __init__(self, **kwargs):
        super(FamilyTreeCanvas, self).__init__(**kwargs)

    def display_info(self, person_id):
        print (person_id)
        person = get_person_info(person_id, self.FIDS2)
        disp = person['name'] + '\n'
        disp+= 'DOB: ' + person['dob']
        disp+= ('        DOD: ' + person['dod']) if (person['dod'] != '') else ''
        disp+= '\n'
        disp+= ('Place of birth: ' + person['pob']) if (person['pob'] != '') else ''

        self.ids.info_disp.text = disp



class Family:
    def __init__(self, id, gen, mum, dad, kids):
        self.id = id
        self.gen = gen
        self.mum = mum
        self.dad = dad
        self.kids = kids
        self.downlinks = []
        self.pos_hint = []
        self.size_hint = []



def get_person_info (person_id, FIDS2):
    if person_id in FIDS2:
        vals = FIDS2[person_id]
        v = {"pid": vals[0],"firstname": vals[1],"surname": vals[2],"name": vals[1] + ' ' + vals[2],"dob": vals[3],"dod": vals[4],"pob": vals[5],"gender": vals[6],
            "mother": vals[7],"father": vals[8]}
        return v
    else:
        print ("PersonID not found in FIDS2")
        v = {"pid": person_id,"firstname": 'NA',"surname": 'NA',"name": 'Not found',"dob": '0',"dod": '0',"pob": 'NA',"gender": 'NA',"mother": 'NA',"father": 'NA'}
        return v




def buildgeneration (g, sibgeneration, families, box_w, sibgroup_gap, sib_gap, y_axis_factor, info_disp_units):
    poscursor = sibgroup_gap
    gen_string = ''
    y_pos = y_axis_factor * (g + info_disp_units)
    for sibgp in sibgeneration:
        for sib in sibgp:
            fam = families.get(sib) # a Family object
            mum = fam.mum       # a dictionary
            dad = fam.dad       # a dictionary
            kids = fam.kids     # a list of dictionaries
            fam.size_hint = [box_w, y_axis_factor * 0.5]
            fam.pos_hint = [poscursor, y_pos]
            size_hint = str(box_w) + ", " + str(y_axis_factor * 0.5)
            pos_hint = "{'x':" + str(poscursor) + ", 'y':" + str(y_pos) + "}"
            childrenstring = ''

            famboxstring = '''
        BoxLayout:
            id: '''+ sib +'''
            size_hint: ''' + size_hint + '''
            pos_hint: ''' + pos_hint + '''
            orientation: 'vertical\''''

            parentstring = '''
            BoxLayout:
                Button:
                    id: '''+ mum['pid'] +'''
                    text: \''''+ mum['name'] +''''
                    halign: 'center'
                    text_size: self.width, None
                    font_size: self.height * .24
                    on_press: root.display_info(\'''' + mum['pid'] + '''')
                Button:
                    id: '''+ dad['pid'] +'''
                    text: \''''+ dad['name'] +''''
                    halign: 'center'
                    text_size: self.width, None
                    font_size: self.height * .24
                    on_press: root.display_info(\'''' + dad['pid'] + '''')
            BoxLayout:'''

            for k in kids:
                childrenstring += '''
                Button:
                    id: '''+ k['pid'] +'''
                    text: \''''+ k['firstname'] + '\\n' + k['surname'] + ''''
                    halign: 'center'
                    text_size: self.width, None
                    font_size: self.height * .21
                    on_press: root.display_info(\'''' + k['pid'] + '\')'
                    #font_size: (self.height *.25) if (len(self.text) < 12) else (self.height *.15)

            gen_string += famboxstring + parentstring + childrenstring
            poscursor += (box_w + sib_gap)
        poscursor -= sib_gap     #deduct the sib_gap following final sib in a group, because we add a sibgroup_gap instead (slightly larger)
        poscursor += sibgroup_gap
    return gen_string




def families_dict (FIDS1, FIDS2):
    # families{} - THIS IS THE DICTIONARY FOR STORING INFO ON EACH FAMILY IN THE FAMILY TREE
    families = {}  # a dictionary of Family objects
    # run through FIDS1 and then grab all the extra info from FIDS2 using get_person_info()
    # example of FIDS1:  ['FID11', 2, 'SK1698', 'TK3231', ['DK6984', 'IK8120']]
    # Also, run through FIDS3 and get the connections to other families
    # example of FIDS3:  [1, 'NA9171', 'FID1', 'FID8']
    for item in FIDS1:
        fam_id = item[0]  # the family id
        fam_gen = item[1]  # the generation number of the family
        fam_mum = get_person_info(item[2], FIDS2)  # returns a dictionary for the mother of the family
        fam_dad = get_person_info(item[3], FIDS2)  # returns a dictionary for the father of the family
        fam_kids = []  ##returns a LIST of dictionaries, one for each child of the family
        for kid_id in item[4]:
            fam_kids.append(get_person_info(kid_id, FIDS2))  # returns a dictionary for each child in the family

        # make a Family object with all this info and add it to the families dictionary
        newfam = Family(fam_id, fam_gen, fam_mum, fam_dad, fam_kids)
        families[fam_id] = newfam

    return families



def get_unique_gens (FIDS1):
    # Get some info on the generations of the family tree
    gens = []
    for item in FIDS1:
        gens.append(item[1])  # item 1 is the generation number
    gens.sort()  # sort lowest to highest, eg [-1, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2]
    # adjust all the generation nummbers if needed so that the lowest descendants are at generation 0
    gens_adjust = 0 - gens[0]
    if gens_adjust != 0:
        gens = [element + gens_adjust for element in gens]
        for item in FIDS1:  # adjust them in the FIDS1 list too
            item[1] += gens_adjust

    # unique_gens = Counter(gens).keys()  #eg [0,1,2,3]  - not working. giving a dict_keys object in debugger instead of a list
    unique_gens = [*Counter(gens)]  # googled it and found this way, using "unpacking" with *
    return unique_gens




def gather_generation(g, FIDS1, FIDS3, families, sibgeneration, fid_done, upfams):
    if g == 0 :
        # process generation 0 this way...
        for fid1 in FIDS1:  # loop through FIDS1

            if fid1[1] == g:  # only act where Generation = 0
                id = fid1[0]  # use the family id to look through FIDS3

                for fid3_a in FIDS3:  # loop through FIDS3
                    downfam = fid3_a[3]

                    if (downfam == id):
                        upfam = fid3_a[2]  # gets the upfam id
                        upfam_obj = families.get(upfam)  # gets the Family object of upfam
                        sibs = []  # initialise list to hold sibs ids (all downfams of upfam)

                        for fid3_b in FIDS3:  # loop through FIDS3 again to collect the sibs ids
                            if fid3_b[2] == upfam:
                                downfam = fid3_b[3]
                                downfam_obj = families.get(downfam)  # a Family object
                                linker = fid3_b[1]
                                if downfam_obj.mum.get('pid')==linker:
                                    link_side='mum'
                                else:
                                    link_side='dad'
                                upfam_obj.downlinks.append([downfam, link_side])

                                if downfam not in fid_done:
                                    sibs.append(downfam)
                                    fid_done.append(downfam)  #add this FID to done list so we don't display this family more than once
                        if len(sibs) > 0 :
                            sibgeneration.append(sibs)  # add the sibs group (if its not empty) to the list of sibs groups for this generation (gen 0)
                        upfams.append(upfam)  # store the upfam for this sibs group in the upfams List
    else:
        # process all other generations this way...
        sibgeneration = []  # reset this list
        for fid1 in FIDS1:  # loop through FIDS1
            if (fid1[1] == g) and (fid1[0] not in upfams):  # Add any FID not already in upfams List (because it had no child fams)
                upfams.append(fid1[0])
        thisgenfams = upfams
        upfams = []  # reset this list now to reuse for adding next generation's upfams
        for this_id in thisgenfams:

            for fid3 in FIDS3:  # loop through FIDS3 to see if there is an entry linking it to an upfam

                if fid3[3] == this_id:
                    upfam = fid3[2]  # gets the upfam id
                    upfam_obj = families.get(upfam)  # gets the Family object of upfam
                    downfam_obj = families.get(this_id)  # a Family object
                    linker = fid3[1]
                    if downfam_obj.mum.get('pid') == linker:
                        link_side = 'mum'
                    else:
                        link_side = 'dad'
                    upfam_obj.downlinks.append([this_id, link_side])
                    upfams.append(upfam)  # store the upfam for this fam id in the upfams List
            if this_id not in fid_done:  # FIDS3 entry found for this_id
                lone_sib = []
                lone_sib.append(this_id)
                sibgeneration.append(
                    lone_sib)  # add the sibs group (only 1 fam) to the list of sibs groups for this generation (g)
                fid_done.append(this_id)  # add this_id to done list so we don't display it more than once

    return sibgeneration, fid_done, upfams





def calculate_sizings(sib_gap_units, sibgroup_gap_units, sibgeneration):
    n = (len(sibgeneration) + 1) * sibgroup_gap_units  # start with no of units between sibling family groups (inc. either side)
    for sibgroup in sibgeneration:
        n = n + (len(sibgroup) + ((len(sibgroup) - 1) * sib_gap_units))  # add a unit per sibling family and gap units between them

    box_w = 1 / n  # calculate ACTUAL screen width for a family-box unit (percentage value where 1 = 100%). Round to 2dp
    sib_gap = round(box_w * sib_gap_units, 2)  # ACTUAL
    sibgroup_gap = round(box_w * sibgroup_gap_units, 2)  # ACTUAL
    return box_w, sib_gap, sibgroup_gap



def assemble_kivy_string(y_axis_factor, info_disp_units, info_text_height, buildgens, families):
    rootstring = '<FamilyTreeCanvas>:'

    topboxstring = '''
    RelativeLayout:
        id: top
        Label:
            id: info_disp
            pos_hint: {'x':0.01, 'y':0.01}
            size_hint: 1, ''' + str(y_axis_factor * info_disp_units) + '''
            text_size: root.width, ''' + str(info_text_height) + '''
            text:'click on a person to see more information'
            color: 1,1,1,1 '''

    generationstring = ''
    for b in buildgens:
        generationstring += b

    # Add lines
    linestring = '''
    RelativeLayout:
        id: lines'''

    for fam in families.values():
        if len(fam.downlinks) > 0:
            up_pos = fam.pos_hint
            up_size = fam.size_hint
            reltop_x = up_pos[0] + (up_size[0] * 0.5)
            reltop_y = up_pos[1]

            for df in fam.downlinks:
                down_id = df[0]
                down_side = df[1]
                downfam_obj = families.get(down_id)
                down_pos = downfam_obj.pos_hint
                down_size = downfam_obj.size_hint
                relpos_x = (down_pos[0] + (down_size[0] * 0.25)) if down_side == 'mum' else (
                            down_pos[0] + (down_size[0] * 0.75))
                relpos_y = down_pos[1] + down_size[1]
                relpos = "{'x':" + str("{0:.2f}".format(relpos_x)) + ", 'y':" + str("{0:.2f}".format(relpos_y)) + "}"
                relsize = str("{0:.2f}".format(reltop_x - relpos_x)) + ", " + str("{0:.2f}".format(reltop_y - relpos_y))
                line_col = '1, 0.75, 0.79, 1' if down_side == 'mum' else '.52, 0.8, 0.98, 1'
                linestring += '''
        BoxLayout:
            id: line_''' + fam.id + '''
            pos_hint: ''' + relpos + '''
            size_hint: ''' + relsize + '''
            canvas:
                Color:
                    rgba: ''' + line_col + '''
                Line:
                    points: self.x, self.y, self.right, self.top
                    width: 2'''

    fullstring = rootstring + linestring + topboxstring + generationstring
    return fullstring




# ============== MAIN SUBROUTINE. CALLED WITH PARAMETERS FIDS1, FIDS2, FIDS3  ===================================================

def draw_family_tree(FIDS1, FIDS2, FIDS3):
    # FIDS1 example :  ['FID11', 0, 'SK1698', 'TK3231', ['DK6984', 'IK8120']]     [familyid, generation, motherid, fatherid, [kids ids]]
    # FIDS2 example :  'FQ2854': ('FQ2854', 'Faizan', 'Qureshi', '2011-11-30', '1908-01-01', 'Cardiff', 'Male', 'SK3438', 'JQ5803')  Person: Person, Firstnm, Surnmm, dob, dod, pob, gender, mother, father
    # FIDS3 example : [1, 'NA9171', 'FID1', 'FID8']      [ignore, linking person, upfam id, downfam id]

    # Using the FIDS1 List make a family object for each fam and put them all in the 'families' dictionary
    families = families_dict(FIDS1, FIDS2)
    # Get a list of generation numbers (levels) for this family tree
    unique_gens = get_unique_gens(FIDS1)

    # For each generation number (0 to n) make a List of families belonging to it
    sibgeneration = []  # The list for the generation
    fid_done = []  # keep track of families in the family tree that have been processed.
    upfams = []  # List of parent families in the next generation up
    buildgens = []  # This will hold the Kivy language strings describing each generatiom, later parsed by Kivy Builder function.

    # Set some sizes for on-screen spaces between family boxes and the information display area at screen bottom
    sib_gap_units = 0.35
    sibgroup_gap_units = 0.7
    info_disp_units = 0.5  # as a proportion (0 to 1) of height of generation rows. Governs height of area at screen bottom
    y_axis_units = len(
        unique_gens) + info_disp_units  # how many units to divide the root (RelativeLayout) height by
    y_axis_factor = round(1 / y_axis_units, 2)  # ACTUAL height of generation rows, as a proportion (0 to 1) of root (RelativeLayout) height
    info_text_height = Window.height * (y_axis_factor * info_disp_units)  # ACTUAL height of info display text in pixels

    # Now process each generation and construct the Kivy code string
    for g in unique_gens:
        # 1. Find all fams in generation 'g' (sibgeneration) and also their immediate ancestor fams (upfams)
        sibgeneration, fid_done, upfams = gather_generation(g, FIDS1, FIDS3, families, sibgeneration,
                                                              fid_done, upfams)
        # 2. Calculate how to fit them across the screen based on num of fams in the generation
        box_w, sib_gap, sibgroup_gap = calculate_sizings(sib_gap_units, sibgroup_gap_units, sibgeneration)
        # 3. Construct a 'kivy code' string for this generation using the above information
        buildgen = buildgeneration(g, sibgeneration, families, box_w, sibgroup_gap, sib_gap, y_axis_factor,
                                   info_disp_units)
        # 4. Add the string for each generation into a list (buildgens)
        buildgens.append(buildgen)

    # Assemble the full string including connecting lines and information display area
    fullstring = assemble_kivy_string(y_axis_factor, info_disp_units, info_text_height, buildgens, families)

    # PASS TO THE KIVY BUILDER FUNCTION
    Builder.load_string(fullstring)

    FamilyTreeCanvas.FIDS2 = FIDS2

# ===================================   END  ===================================================


# ================== KIVY APP IS KICKED OFF BY CREATING A STARTER CLASS WHICH INHERITS FROM KIVY.APP ===================
class StartFamilyTreeApp(App):
    def build(self):
        draw_family_tree(self.fids1, self.fids2, self.fids3)
        return FamilyTreeCanvas()

# ===================================   END  ===================================================


if __name__ == "__main__":
    pass    # do nothing if running this module directly
    #StartFamilyTreeApp().run()