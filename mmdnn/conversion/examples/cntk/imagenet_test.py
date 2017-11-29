# Copyright (c) Microsoft. All rights reserved.

# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

import argparse
import numpy as np
import sys
import os
import cntk as C
from mmdnn.conversion.examples.imagenet_test import TestKit

class TestCNTK(TestKit):

    def __init__(self):
        super(TestCNTK, self).__init__()
        
        self.truth['keras']['resnet'] = [(144, 0.77398175), (23, 0.10650793), (21, 0.081077583), (146, 0.0092755388), (562, 0.0089645367)]
        self.truth['tensorflow']['resnet'] = [(22, 13.589937), (147, 8.9272985), (90, 5.7173862), (24, 5.7097111), (88, 4.77315)]
        
        self.model = self.MainModel.KitModel(self.args.w)
        # self.model, self.testop = self.MainModel.KitModel(self.args.w)


    def preprocess(self, image_path):
        self.data = super(TestCNTK, self).preprocess(image_path)        


    def print_result(self):
        predict = self.model.eval({self.model.arguments[0]:[self.data]})
        super(TestCNTK, self).print_result(predict)
        
    
    def print_intermediate_result(self, layer_name, if_transpose = False):
        test_arr = self.testop.eval({self.testop.arguments[0]:[self.data]})
        super(TestCNTK, self).print_intermediate_result(test_arr, if_transpose)

    
    def inference(self, image_path):
        self.preprocess(image_path)
        
        # self.print_intermediate_result(None, False)
        
        self.print_result()
        
        self.test_truth()

    def dump(self, path = None):
        if path is None: path = self.args.dump
        self.model.save(path)
        print ('CNTK model file is saved as [{}], generated by [{}.py] and [{}].'.format(
            path, self.args.n, self.args.w))


if __name__=='__main__':   
    tester = TestCNTK()
    if tester.args.dump:
        tester.dump()
    else:
        tester.inference(tester.args.image)