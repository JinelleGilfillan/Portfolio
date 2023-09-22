# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
import numpy as np
import os
import math
from RavensFigure import RavensFigure
from RavensObject import RavensObject


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self, problem):
        type = problem.problemType
        if not problem.hasVerbal:
            if type == "2x2":
                answer, conf = self.visual2(problem)
            elif type == "3x3":
                answer, conf = self.visual3(problem)
        elif type == "2x2":
            answer1, conf1 = self.two(problem)
            answer2, conf2 = self.visual2(problem)
            if answer1 == answer2:
                answer = answer1
            else:
                if conf1 >= conf2:
                    answer = answer1
                else:
                    answer = answer2
        elif type == "3x3":
            answer1, conf1 = self.three(problem)
            answer2, conf2 = self.visual3(problem)
            if answer1 == answer2:
                answer = answer1
            else:
                if conf1 >= conf2:
                    answer = answer1
                else:
                    answer = answer2
        else:
            answer = 0

        return answer

    def visual2(self, problem):
        figures_list = list(problem.figures.keys())
        image1 = np.array(Image.open(
            "Problems" + os.sep + problem.problemSetName + os.sep + problem.name + os.sep + "A.png"))
        flip_image1 = np.array(Image.open(
            "Problems" + os.sep + problem.problemSetName + os.sep + problem.name + os.sep + "A.png").transpose(
            Image.FLIP_LEFT_RIGHT))
        image2 = np.array(Image.open(
            "Problems" + os.sep + problem.problemSetName + os.sep + problem.name + os.sep + "B.png"))

        # Use mean squared error (MSE) to compare the two figures
        mse1 = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
        mse1 /= float(image1.shape[0] * image2.shape[1])

        # Then compare each value in options to see if which one has the closest mse
        image3 = np.array(Image.open(
            "Problems" + os.sep + problem.problemSetName + os.sep + problem.name + os.sep + "C.png"))

        mse2 = np.sum((image1.astype("float") - image3.astype("float")) ** 2)
        mse2 /= float(image1.shape[0] * image3.shape[1])

        closest_mse = 100000000000000
        returnval = -1
        for i in range(len(figures_list)):
            if figures_list[i].isdigit():
                image4 = np.array(Image.open(
                    "Problems" + os.sep + problem.problemSetName + os.sep + problem.name + os.sep + str(
                        figures_list[i]) + ".png"))

                # Use mean squared error (MSE) to compare the two figures
                test_mse1 = np.sum((image3.astype("float") - image4.astype("float")) ** 2)
                test_mse1 /= float(image3.shape[0] * image4.shape[1])

                test_mse2 = np.sum((image2.astype("float") - image4.astype("float")) ** 2)
                test_mse2 /= float(image2.shape[0] * image4.shape[1])

                if math.sqrt((mse1 - test_mse1) ** 2 + (mse2 - test_mse2) ** 2) < closest_mse:
                    closest_mse = math.sqrt((mse1 - test_mse1) ** 2 + (mse2 - test_mse2) ** 2)
                    returnval = figures_list[i]

        if closest_mse == 0:
            confidence = 1
        else:
            confidence = .65

        return int(returnval), confidence

    def visual3(self, problem):
        figures_list = list(problem.figures.keys())
        im1 = Image.open(
            "Problems" + os.sep + problem.problemSetName + os.sep + problem.name + os.sep + "A.png")
        im2 = Image.open(
            "Problems" + os.sep + problem.problemSetName + os.sep + problem.name + os.sep + "B.png")
        im3 = Image.open(
            "Problems" + os.sep + problem.problemSetName + os.sep + problem.name + os.sep + "C.png")
        thresh = 200
        fractures = 16

        similarity_list = []

        # Test between image 1 and 2
        keyword, mse1 = self.fractal(im1, im2, thresh, fractures)
        #print(keyword, mse1)
        similarity_list.append(keyword)

        # Test between image 2 and 3
        keyword, mse2 = self.fractal(im2, im3, thresh, fractures)
        #print(keyword, mse2)
        similarity_list.append(keyword)

        # Then compare each value in options to see if which one has the closest mse
        im4 = Image.open(
            "Problems" + os.sep + problem.problemSetName + os.sep + problem.name + os.sep + "D.png")
        im5 = Image.open(
            "Problems" + os.sep + problem.problemSetName + os.sep + problem.name + os.sep + "E.png")
        im6 = Image.open(
            "Problems" + os.sep + problem.problemSetName + os.sep + problem.name + os.sep + "F.png")

        keyword, mse3 = self.fractal(im4, im5, thresh, fractures)
        #print(keyword, mse3)
        similarity_list.append(keyword)
        keyword, mse4 = self.fractal(im5, im6, thresh, fractures)
        #print(keyword, mse4)
        similarity_list.append(keyword)

        im7 = Image.open(
            "Problems" + os.sep + problem.problemSetName + os.sep + problem.name + os.sep + "G.png")
        im8 = Image.open(
            "Problems" + os.sep + problem.problemSetName + os.sep + problem.name + os.sep + "H.png")

        keyword, mse5 = self.fractal(im7, im8, thresh, fractures)
        #print(keyword, mse5)
        similarity_list.append(keyword)

        keyword, mse6 = self.fractal(im1, im4, thresh, fractures)
        #print(keyword, mse6)
        similarity_list.append(keyword)
        keyword, mse7 = self.fractal(im4, im7, thresh, fractures)
        #print(keyword, mse7)
        similarity_list.append(keyword)

        keyword, mse8 = self.fractal(im2, im5, thresh, fractures)
        #print(keyword, mse8)
        similarity_list.append(keyword)
        keyword, mse9 = self.fractal(im5, im8, thresh, fractures)
        #print(keyword, mse9)
        similarity_list.append(keyword)

        keyword, mse10 = self.fractal(im3, im6, thresh, fractures)
        #print(keyword, mse10)
        similarity_list.append(keyword)

        # Test between diagonals
        keyword, dmse1 = self.fractal(im1, im5, thresh, fractures)
        #print(keyword, dmse1)
        similarity_list.append(keyword)

        keyword, dmse2 = self.fractal(im2, im6, thresh, fractures)
        #print(keyword, dmse2)
        similarity_list.append(keyword)

        keyword, dmse3 = self.fractal(im4, im8, thresh, fractures)
        #print(keyword, dmse3)
        similarity_list.append(keyword)

        # print(similarity_list)
        closest_mse = 100000000000000
        returnval = -1
        for i in range(len(figures_list)):
            if figures_list[i].isdigit():
                im9 = Image.open(
                    "Problems" + os.sep + problem.problemSetName + os.sep + problem.name + os.sep + str(
                        figures_list[i]) + ".png")

                # Use mean squared error (MSE) to compare the two figures
                keyword, test_mse1 = self.fractal(im8, im9, thresh, fractures)

                keyword, test_mse2 = self.fractal(im6, im9, thresh, fractures)

                keyword, test_mse3 = self.fractal(im5, im9, thresh, fractures)
                # print("Option: "+str(figures_list[i]))
                # print("test MSE 1: " + str(test_mse1))
                # print("test MSE 2: " + str(test_mse1))
                # print("test MSE 3: " + str(test_mse3))

                calc = math.sqrt((((((mse1 + mse2) / 2) + ((mse3 + mse4) / 2)) / 2) - ((mse5 + test_mse1) / 2)) ** 2 +
                                 (((((mse6 + mse7) / 2) + ((mse8 + mse9) / 2)) / 2) - ((mse10 + test_mse2) / 2)) ** 2 +
                                 (((dmse1 + dmse2 + dmse3)/3) - test_mse3) ** 2)

                #print("Calc: " + str(calc))

                if calc < closest_mse:
                    closest_mse = calc
                    returnval = figures_list[i]

        if closest_mse == 0:
            confidence = 1
        else:
            confidence = .65
        return int(returnval), confidence

    def two(self, problem):
        figures_dict = problem.figures
        return_val = -1
        max_num = -1

        # Check to see if A or C
        # First complete for A
        previous_obj_names = list(figures_dict['A'].objects.keys())
        previous_obj_count = len(previous_obj_names)
        if previous_obj_count > 0:
            previous_attr = [list(list(figures_dict['A'].objects.values())[0].attributes.items())]
        else:
            previous_attr = []
        for k in range(previous_obj_count):
            if k != 0:
                previous_attr.append(
                    list(list(figures_dict['A'].objects.values())[k].attributes.items()))

        # Check again previous obj, get transformative descriptions
        current_obj_names = list(figures_dict['B'].objects.keys())
        current_obj_count = len(current_obj_names)
        if current_obj_count > 0:
            current_attr = [list(list(figures_dict['B'].objects.values())[0].attributes.items())]
        else:
            current_attr = []
        for k in range(current_obj_count):
            if k != 0:
                current_attr.append(
                    list(list(figures_dict['B'].objects.values())[k].attributes.items()))
        trans_list_1 = self.checks(previous_obj_names, current_obj_names, previous_obj_count, current_obj_count,
                                   previous_attr, current_attr)

        # Complete for C
        previous_obj_names = list(figures_dict['C'].objects.keys())
        previous_obj_count = len(previous_obj_names)
        if previous_obj_count > 0:
            previous_attr = [list(list(figures_dict['C'].objects.values())[0].attributes.items())]
        else:
            previous_attr = []
        for k in range(previous_obj_count):
            if k != 0:
                previous_attr.append(
                    list(list(figures_dict['C'].objects.values())[k].attributes.items()))

        for i in range(len(list(figures_dict.keys()))):
            if list(figures_dict.keys())[i].isdigit():
                # Check against previous obj, get transformative descriptions, check for differences again trans_list_1
                current_obj_names = list(list(figures_dict.values())[i].objects.keys())
                current_obj_count = len(current_obj_names)

                if current_obj_count > 0:
                    current_attr = [list(list(list(figures_dict.values())[i].objects.values())[0].attributes.items())]
                else:
                    current_attr = []

                for k in range(current_obj_count):
                    if k != 0:
                        current_attr.append(
                            list(list(list(figures_dict.values())[i].objects.values())[k].attributes.items()))

                trans_list_2 = self.checks(previous_obj_names, current_obj_names, previous_obj_count, current_obj_count,
                                           previous_attr, current_attr)

                num = 0
                for j in range(len(trans_list_1)):
                    for k in range(len(trans_list_2)):
                        if trans_list_1[j][0] == trans_list_2[k][0]:
                            num += trans_list_1[j][1]
                # print(list(figures_dict.keys())[i])
                # print(trans_list_1)
                # print(trans_list_2)
                # print(num)
                if num > max_num:
                    max_num = num
                    return_val = list(figures_dict.keys())[i]

        total_count = 0
        for c in range(len(trans_list_1)):
            total_count += trans_list_1[c][1]
        confidence = max_num / total_count

        return int(return_val), confidence

    def three(self, problem):
        figures_dict = problem.figures
        return_val = -1
        max_num = -1

        # First complete for A
        previous_obj_names = list(figures_dict['A'].objects.keys())
        previous_obj_count = len(previous_obj_names)
        if previous_obj_count > 0:
            previous_attr = [list(list(figures_dict['A'].objects.values())[0].attributes.items())]
        else:
            previous_attr = []
        for k in range(previous_obj_count):
            if k != 0:
                previous_attr.append(
                    list(list(figures_dict['A'].objects.values())[k].attributes.items()))

        # Then complete for B, and compare the two
        current_obj_names = list(figures_dict['B'].objects.keys())
        current_obj_count = len(current_obj_names)
        if current_obj_count > 0:
            current_attr = [list(list(figures_dict['B'].objects.values())[0].attributes.items())]
        else:
            current_attr = []
        for k in range(current_obj_count):
            if k != 0:
                current_attr.append(
                    list(list(figures_dict['B'].objects.values())[k].attributes.items()))
        trans_list_1 = self.checks(previous_obj_names, current_obj_names, previous_obj_count, current_obj_count,
                                   previous_attr, current_attr)

        # Next compare B to C
        next_obj_names = list(figures_dict['C'].objects.keys())
        next_obj_count = len(next_obj_names)
        if next_obj_count > 0:
            next_attr = [list(list(figures_dict['C'].objects.values())[0].attributes.items())]
        else:
            next_attr = []
        for k in range(next_obj_count):
            if k != 0:
                next_attr.append(
                    list(list(figures_dict['C'].objects.values())[k].attributes.items()))
        trans_list_2 = self.checks(current_obj_names, next_obj_names, current_obj_count, next_obj_count,
                                   current_attr, next_attr)

        row_1 = trans_list_1 + trans_list_2
        # print(row_1)

        # Complete for the second row
        # First complete for D
        previous_obj_names = list(figures_dict['D'].objects.keys())
        previous_obj_count = len(previous_obj_names)
        if previous_obj_count > 0:
            previous_attr = [list(list(figures_dict['D'].objects.values())[0].attributes.items())]
        else:
            previous_attr = []
        for k in range(previous_obj_count):
            if k != 0:
                previous_attr.append(
                    list(list(figures_dict['D'].objects.values())[k].attributes.items()))

        # Then complete for E, and compare the two
        current_obj_names = list(figures_dict['E'].objects.keys())
        current_obj_count = len(current_obj_names)
        if current_obj_count > 0:
            current_attr = [list(list(figures_dict['E'].objects.values())[0].attributes.items())]
        else:
            current_attr = []
        for k in range(current_obj_count):
            if k != 0:
                current_attr.append(
                    list(list(figures_dict['E'].objects.values())[k].attributes.items()))
        trans_list_1 = self.checks(previous_obj_names, current_obj_names, previous_obj_count, current_obj_count,
                                   previous_attr, current_attr)

        # Next compare E to F
        next_obj_names = list(figures_dict['F'].objects.keys())
        next_obj_count = len(next_obj_names)
        if next_obj_count > 0:
            next_attr = [list(list(figures_dict['F'].objects.values())[0].attributes.items())]
        else:
            next_attr = []
        for k in range(next_obj_count):
            if k != 0:
                next_attr.append(
                    list(list(figures_dict['F'].objects.values())[k].attributes.items()))
        trans_list_2 = self.checks(current_obj_names, next_obj_names, current_obj_count, next_obj_count,
                                   current_attr, next_attr)

        row_2 = trans_list_1 + trans_list_2
        # print(row_2)

        # find similarities between the two rows to keep for checking
        row = []
        for a in range(len(row_1)):
            for b in range(len(row_2)):
                if row_1[a] == row_2[b]:
                    row.append((row_1[a][0], row_1[a][1] * 2))
                else:
                    row.append(row_1[a])

        # complete same thing for columns
        # First complete for A
        previous_obj_names = list(figures_dict['A'].objects.keys())
        previous_obj_count = len(previous_obj_names)
        if previous_obj_count > 0:
            previous_attr = [list(list(figures_dict['A'].objects.values())[0].attributes.items())]
        else:
            previous_attr = []
        for k in range(previous_obj_count):
            if k != 0:
                previous_attr.append(
                    list(list(figures_dict['A'].objects.values())[k].attributes.items()))

        # Then complete for D, and compare the two
        current_obj_names = list(figures_dict['D'].objects.keys())
        current_obj_count = len(current_obj_names)
        if current_obj_count > 0:
            current_attr = [list(list(figures_dict['D'].objects.values())[0].attributes.items())]
        else:
            current_attr = []
        for k in range(current_obj_count):
            if k != 0:
                current_attr.append(
                    list(list(figures_dict['D'].objects.values())[k].attributes.items()))
        trans_list_1 = self.checks(previous_obj_names, current_obj_names, previous_obj_count, current_obj_count,
                                   previous_attr, current_attr)

        # Next compare D to G
        next_obj_names = list(figures_dict['G'].objects.keys())
        next_obj_count = len(next_obj_names)
        if next_obj_count > 0:
            next_attr = [list(list(figures_dict['G'].objects.values())[0].attributes.items())]
        else:
            next_attr = []
        for k in range(next_obj_count):
            if k != 0:
                next_attr.append(
                    list(list(figures_dict['G'].objects.values())[k].attributes.items()))
        trans_list_2 = self.checks(current_obj_names, next_obj_names, current_obj_count, next_obj_count,
                                   current_attr, next_attr)

        column_1 = trans_list_1 + trans_list_2
        # print(column_1)

        # Complete for the second column
        # First complete for B
        previous_obj_names = list(figures_dict['B'].objects.keys())
        previous_obj_count = len(previous_obj_names)
        if previous_obj_count > 0:
            previous_attr = [list(list(figures_dict['B'].objects.values())[0].attributes.items())]
        else:
            previous_attr = []
        for k in range(previous_obj_count):
            if k != 0:
                previous_attr.append(
                    list(list(figures_dict['B'].objects.values())[k].attributes.items()))

        # Then complete for E, and compare the two
        current_obj_names = list(figures_dict['E'].objects.keys())
        current_obj_count = len(current_obj_names)
        if current_obj_count > 0:
            current_attr = [list(list(figures_dict['E'].objects.values())[0].attributes.items())]
        else:
            current_attr = []
        for k in range(current_obj_count):
            if k != 0:
                current_attr.append(
                    list(list(figures_dict['E'].objects.values())[k].attributes.items()))
        trans_list_1 = self.checks(previous_obj_names, current_obj_names, previous_obj_count, current_obj_count,
                                   previous_attr, current_attr)

        # Next compare E to H
        next_obj_names = list(figures_dict['H'].objects.keys())
        next_obj_count = len(next_obj_names)
        if next_obj_count > 0:
            next_attr = [list(list(figures_dict['H'].objects.values())[0].attributes.items())]
        else:
            next_attr = []
        for k in range(next_obj_count):
            if k != 0:
                next_attr.append(
                    list(list(figures_dict['H'].objects.values())[k].attributes.items()))
        trans_list_2 = self.checks(current_obj_names, next_obj_names, current_obj_count, next_obj_count,
                                   current_attr, next_attr)

        column_2 = trans_list_1 + trans_list_2
        # print(column_2)

        # find similarities between the two columns to keep for checking
        column = []
        for a in range(len(column_1)):
            for b in range(len(column_2)):
                if column_1[a] == column_2[b]:
                    column.append((column_1[a][0], column_1[a][1] * 2))
                else:
                    column.append(column_1[a])

        # Complete for G, H; C, F then each number and then compare the row and column
        previous_obj_names = list(figures_dict['G'].objects.keys())
        previous_obj_count = len(previous_obj_names)
        if previous_obj_count > 0:
            previous_attr = [list(list(figures_dict['G'].objects.values())[0].attributes.items())]
        else:
            previous_attr = []
        for k in range(previous_obj_count):
            if k != 0:
                previous_attr.append(
                    list(list(figures_dict['G'].objects.values())[k].attributes.items()))

        current_obj_names = list(figures_dict['H'].objects.keys())
        current_obj_count = len(current_obj_names)
        if current_obj_count > 0:
            current_attr = [list(list(figures_dict['H'].objects.values())[0].attributes.items())]
        else:
            current_attr = []
        for k in range(current_obj_count):
            if k != 0:
                current_attr.append(
                    list(list(figures_dict['H'].objects.values())[k].attributes.items()))
        row_trans_list_1 = self.checks(previous_obj_names, current_obj_names, previous_obj_count, current_obj_count,
                                       previous_attr, current_attr)

        # Repeat for column
        previous_obj_names = list(figures_dict['C'].objects.keys())
        previous_obj_count = len(previous_obj_names)
        if previous_obj_count > 0:
            previous_attr = [list(list(figures_dict['C'].objects.values())[0].attributes.items())]
        else:
            previous_attr = []
        for k in range(previous_obj_count):
            if k != 0:
                previous_attr.append(
                    list(list(figures_dict['C'].objects.values())[k].attributes.items()))

        current_obj_names = list(figures_dict['F'].objects.keys())
        current_obj_count = len(current_obj_names)
        if current_obj_count > 0:
            current_attr = [list(list(figures_dict['F'].objects.values())[0].attributes.items())]
        else:
            current_attr = []
        for k in range(current_obj_count):
            if k != 0:
                current_attr.append(
                    list(list(figures_dict['F'].objects.values())[k].attributes.items()))
        column_trans_list_1 = self.checks(previous_obj_names, current_obj_names, previous_obj_count, current_obj_count,
                                          previous_attr, current_attr)

        for i in range(len(list(figures_dict.keys()))):
            if list(figures_dict.keys())[i].isdigit():
                # Check against previous obj, get transformative descriptions, check for differences again trans_list_1
                next_obj_names = list(list(figures_dict.values())[i].objects.keys())
                next_obj_count = len(next_obj_names)

                if next_obj_count > 0:
                    next_attr = [list(list(list(figures_dict.values())[i].objects.values())[0].attributes.items())]
                else:
                    next_attr = []

                for k in range(next_obj_count):
                    if k != 0:
                        next_attr.append(
                            list(list(list(figures_dict.values())[i].objects.values())[k].attributes.items()))

                row_trans_list_2 = self.checks(current_obj_names, next_obj_names, current_obj_count,
                                               next_obj_count, current_attr, next_attr)
                row_check = row_trans_list_1 + row_trans_list_2

                # Repeat for columns
                # Check against previous obj, get transformative descriptions,
                # check for differences again trans_list_1

                column_trans_list_2 = self.checks(current_obj_names, next_obj_names, current_obj_count,
                                                  next_obj_count, current_attr, next_attr)
                column_check = column_trans_list_1 + column_trans_list_2

                # print(list(figures_dict.keys())[i])
                # print(row)
                # print(row_check)
                # print(column)
                # print(column_check)
                num = 0
                for j in range(len(row)):
                    for k in range(len(row_check)):
                        if row[j][0] == row_check[k][0]:
                            num += row[j][1]

                for j in range(len(column)):
                    for k in range(len(column_check)):
                        if column[j][0] == column_check[k][0]:
                            num += column[j][1]

                if num > max_num:
                    max_num = num
                    return_val = list(figures_dict.keys())[i]

        total_count = 0
        for c in range(len(row)):
            total_count += row[c][1]
        for d in range(len(column)):
            total_count += column[d][1]
        confidence = max_num / total_count

        return int(return_val), confidence

    def checks(self, previous_obj_names, current_obj_names, previous_obj_count, current_obj_count,
               previous_attr, current_attr):
        # function for performing checks and generating string
        trans_list_1 = []
        if previous_obj_names == current_obj_names:
            keyword = ("same object names", 1)
        else:
            keyword = ("different object names", 1)
        trans_list_1.append(keyword)
        if previous_obj_count == current_obj_count:
            keyword = ("same object count", 5)
        elif previous_obj_count > current_obj_count:
            keyword = ("decrease object count", 5)
            decrease_count = previous_obj_count - current_obj_count
        elif previous_obj_count < current_obj_count:
            keyword = ("increase object count", 5)
            increase_count = current_obj_count - previous_obj_count
        trans_list_1.append(keyword)
        if previous_attr == current_attr:
            sorted_list = self.sort_list(previous_attr, previous_obj_names)
            previous_sorted = sorted(sorted_list, key=lambda x: x[1])
            sorted_list = self.sort_list(current_attr, current_obj_names)
            current_sorted = sorted(sorted_list, key=lambda x: x[1])
            keywords = self.find_keywords(previous_attr, previous_sorted, current_attr, current_sorted)
            for each in range(len(keywords)):
                trans_list_1.append(keywords[each])
        elif keyword[0] == "same object count":
            sorted_list = self.sort_list(previous_attr, previous_obj_names)
            previous_sorted = sorted(sorted_list, key=lambda x: x[1])
            sorted_list = self.sort_list(current_attr, current_obj_names)
            current_sorted = sorted(sorted_list, key=lambda x: x[1])
            keywords = self.find_keywords(previous_attr, previous_sorted, current_attr, current_sorted)
            for each in range(len(keywords)):
                trans_list_1.append(keywords[each])

        elif keyword[0] == "decrease object count":
            for count in range(decrease_count):
                keyword = (str(count) + " objectdeleted", 3)
                trans_list_1.append(keyword)

            sorted_list = self.sort_list(previous_attr, previous_obj_names)
            previous_sorted = sorted(sorted_list, key=lambda x: x[1])
            sorted_list = self.sort_list(current_attr, current_obj_names)
            current_sorted = sorted(sorted_list, key=lambda x: x[1])
            keywords = self.find_keywords(previous_attr, previous_sorted, current_attr, current_sorted)
            for each in range(len(keywords)):
                trans_list_1.append(keywords[each])

        else:
            for count in range(increase_count):
                keyword = (str(count) + " objectadded", 3)
                trans_list_1.append(keyword)

            sorted_list = self.sort_list(previous_attr, previous_obj_names)
            previous_sorted = sorted(sorted_list, key=lambda x: x[1])
            sorted_list = self.sort_list(current_attr, current_obj_names)
            current_sorted = sorted(sorted_list, key=lambda x: x[1])
            keywords = self.find_keywords(previous_attr, previous_sorted, current_attr, current_sorted)
            for each in range(len(keywords)):
                trans_list_1.append(keywords[each])

        return trans_list_1

    def find_keywords(self, previous_attr, previous_sorted, current_attr, current_sorted):
        keyword_list = []
        if len(previous_attr) < len(current_attr):
            iterater = len(previous_attr)
        else:
            iterater = len(current_attr)
        for a in range(iterater):
            prev_dict = dict(previous_attr[previous_sorted[a][0]])
            curr_dict = dict(current_attr[current_sorted[a][0]])
            pattr_list = list(prev_dict.keys())
            cattr_list = list(curr_dict.keys())
            for c in range(len(pattr_list)):
                if pattr_list[c] == "size" and prev_dict.get("shape") == "square":
                    pattr_list[c] = "width"
                    pattr_list.append("height")
                    prev_dict["width"] = prev_dict["size"]
                    prev_dict["height"] = prev_dict["size"]
                    del prev_dict["size"]
            for c in range(len(cattr_list)):
                if cattr_list[c] == "size" and curr_dict.get("shape") == "square":
                    cattr_list[c] = "width"
                    cattr_list.append("height")
                    curr_dict["width"] = curr_dict["size"]
                    curr_dict["height"] = curr_dict["size"]
                    del curr_dict["size"]
            for b in range(len(pattr_list)):
                if pattr_list[b] in cattr_list:
                    if prev_dict[pattr_list[b]] == curr_dict[pattr_list[b]]:
                        keyword = (str(a) + " same " + str(pattr_list[b]), 1)
                    else:
                        # print(pattr_list[b])
                        if curr_dict[pattr_list[b]].isdigit() and prev_dict[pattr_list[b]].isdigit():
                            difference_val = abs(
                                int(curr_dict[pattr_list[b]]) - int(prev_dict[pattr_list[b]]))
                            keyword = (
                                str(a) + " " + str(pattr_list[b]) + " value difference " + str(difference_val), 3)
                        elif pattr_list[b] == "size" or pattr_list[b] == "width" or pattr_list[b] == "height":
                            switcher = {
                                "huge": 6,
                                "very large": 5,
                                "large": 4,
                                "medium": 3,
                                "small": 2,
                                "very small": 1
                            }
                            sizediff = switcher.get(curr_dict[pattr_list[b]], 0) - switcher.get(
                                prev_dict[pattr_list[b]])
                            keyword = (str(a) + " " + str(pattr_list[b]) + " difference is " + str(sizediff), 3)
                        else:
                            transform = ""
                            if len(curr_dict[pattr_list[b]]) <= len(prev_dict[pattr_list[b]]):
                                for e in range(len(curr_dict[pattr_list[b]])):
                                    if curr_dict[pattr_list[b]][e] != prev_dict[pattr_list[b]][e]:
                                        transform = transform + str(curr_dict[pattr_list[b]][e])
                            else:
                                for e in range(len(prev_dict[pattr_list[b]])):
                                    if curr_dict[pattr_list[b]][e] != prev_dict[pattr_list[b]][e]:
                                        transform = transform + str(curr_dict[pattr_list[b]][e])
                                for e in range(len(prev_dict[pattr_list[b]]), len(curr_dict[pattr_list[b]])):
                                    transform = transform + str(curr_dict[pattr_list[b]][e])
                            keyword = (str(a) + " " + str(pattr_list[b]) + " transformed into " + transform, 1)

                    keyword_list.append(keyword)
                else:
                    keyword = ("missing attribute " + pattr_list[b], 1)
                    keyword_list.append(keyword)

            for b in range(len(cattr_list)):
                if cattr_list[b] not in pattr_list:
                    keyword = ("added attribute " + cattr_list[b], 1)

                    keyword_list.append(keyword)
        return keyword_list

    def sort_list(self, attribute_list, object_names):
        sorted_list = []
        for a in range(len(attribute_list)):
            length = len(attribute_list[a])
            attributes = list(dict(attribute_list[a]))
            if attributes.count("inside") > 0:
                length += len(list(dict(attribute_list[a]).get('inside')))
            if a == 0:
                sorted_list = [[a, length]]
            else:
                sorted_list.append([a, length])

        for b in range(len(sorted_list)):
            for c in range(len(sorted_list)):
                if sorted_list[b][1] == sorted_list[c][1]:
                    if object_names[sorted_list[b][0]] > object_names[sorted_list[c][0]]:
                        sorted_list[b][1] += 1
                    elif object_names[sorted_list[c][0]] > object_names[sorted_list[b][0]]:
                        sorted_list[c][1] += 1

        for b in range(len(sorted_list)):
            for c in range(len(sorted_list)):
                if sorted_list[b][1] == sorted_list[c][1]:
                    if object_names[sorted_list[b][0]] > object_names[sorted_list[c][0]]:
                        sorted_list[b][1] += 1
                    elif object_names[sorted_list[c][0]] > object_names[sorted_list[b][0]]:
                        sorted_list[c][1] += 1

        return sorted_list

    def fractal(self, im1, im2, thresh, fractures):
        image1 = np.array(im1)
        image1[image1 < thresh] = 0  # Black
        image1[image1 >= thresh] = 255  # White
        image2 = np.array(im2)
        image2[image2 < thresh] = 0  # Black
        image2[image2 >= thresh] = 255  # White

        # Fist check for the transitions over the entire image
        keyword, number = self.checkTransitions(image1, image2)
        if number < 1:
            return keyword, number

        # Use mean squared error (MSE) to compare the two figures
        mse_keyword = "MSE"
        mse1 = np.sum(abs(np.subtract(image1.astype(np.float), image2.astype(np.float))))
        mse1 /= float(im1.width * im1.height)
        mse_number = mse1

        if mse1 < 150:
            return mse_keyword, mse_number
        else:

            # Then check for transitions over the fractures

            m = int(im2.height // math.sqrt(fractures))
            n = int(im2.width // math.sqrt(fractures))

            new_image2 = [image2[x:x + m, y:y + n] for x in range(0, im2.height, m) for y in range(0, im2.width, n)]

            keyword_list = []
            number_list = []

            # For each fracture, check the transitions
            x = new_image2[0].shape[0]
            y = new_image2[0].shape[1]
            for i in range(fractures):
                # Eliminate all white sections
                # print(new_image2[i])
                if not np.all(new_image2[i] == 255):
                    # Look in each section of image 1 to find the most similar match to the fracture in image 2
                    score = 10000000000000
                    final_keyword = ""
                    final_number = 1000000000000000

                    break_val = 0

                    for j in range(im1.height - x):
                        if j % 10 == 0 and break_val == 0:
                            for k in range(im1.width - y):
                                if k % 10 == 0 and break_val == 0:
                                    # split into correct size
                                    new_image1 = image1[j:j + x, k:k + y]
                                    keyword, number = self.checkTransitions(new_image1, new_image2[i])

                                    # If statement to check for the most similar
                                    if number < score:
                                        score = number
                                        final_number = number
                                        final_keyword = keyword
                                        if score < 6:
                                            break_val = 1
                    if final_number < 1000000000000000:
                        keyword_list.append(final_keyword)
                        number_list.append(final_number)
                    else:
                        keyword_list.append("No transition found")
                        number_list.append(50)
                        # Image.fromarray(new_image2[i]).show()

        # If no fractal similarity is found, use MSE
        if all(vals == "No transition found" for vals in keyword_list):
            # Use mean squared error (MSE) to compare the two figures
            return mse_keyword, mse_number
        else:
            return keyword_list, sum(number_list)

    def checkTransitions(self, new_image1, new_image2):
        new_im2 = Image.fromarray(new_image2)
        HF2 = np.array(new_im2.transpose(Image.FLIP_TOP_BOTTOM))
        VF2 = np.array(new_im2.transpose(Image.FLIP_LEFT_RIGHT))
        R45 = np.array(new_im2.rotate(45))
        R90 = np.array(new_im2.rotate(90))
        R135 = np.array(new_im2.rotate(135))
        R180 = np.array(new_im2.rotate(180))
        R225 = np.array(new_im2.rotate(225))
        R270 = np.array(new_im2.rotate(270))

        if np.sum(np.subtract(new_image1, new_image2)) == int(0):
            keyword = "identical"
            number = 0
        # Check for horizontal flip
        elif np.sum(np.subtract(new_image1, HF2)) == int(0):
            keyword = "horizontal flip"
            number = .05
        # Check for vertical flip
        elif np.sum(np.subtract(new_image1, VF2)) == int(0):
            keyword = "vertical flip"
            number = .1
        # Check for 45 degree rotation
        elif np.sum(np.subtract(new_image1, R45)) == int(0):
            keyword = "45 rotation"
            number = .125
        # Check for 90 degree rotation
        elif np.sum(np.subtract(new_image1, R90)) == int(0):
            keyword = "90 rotation"
            number = .15
        # Check for 135 degree rotation
        elif np.sum(np.subtract(new_image1, R135)) == int(0):
            keyword = "135 rotation"
            number = .155
        # Check for 180 degree rotation
        elif np.sum(np.subtract(new_image1, R180)) == int(0):
            keyword = "180 rotation"
            number = .2
        # Check for 225 degree rotation
        elif np.sum(np.subtract(new_image1, R225)) == int(0):
            keyword = "225 rotation"
            number = .225
        # Check for 270 degree rotation
        elif np.sum(np.subtract(new_image1, R270)) == int(0):
            keyword = "270 rotation"
            number = .25
        else:
            keyword = "No transition found"
            diff1 = np.sum(abs(np.subtract(new_image1.astype(np.float), new_image2.astype(np.float))))
            diff1 /= float(new_im2.width * new_im2.height)
            number = diff1

        return keyword, number
