#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import numpy as np


class NumpyHandler(object):
    def __init__(self, dtype):
        self.array_type = np.ndarray
        self.dtype = dtype
        self.size = lambda x: x.size
        self.shape = lambda x: x.shape
        self.reshape = lambda x, s: x.reshape(s)
        self.slice = lambda x, s: x[s]
        self.get = lambda x: x
        self.context = 'numpy'
        self.EMPTY = np.zeros(0)

    def allocate(self, size):
        return np.zeros(size, dtype=self.dtype)

    @staticmethod
    def fill(mem, val):
        mem.fill(val)

    def set_from_numpy(self, mem, arr):
        mem[:] = arr.astype(self.dtype)

    @staticmethod
    def copy_to(dest, src):
        # FIXME: change casting to 'no'
        np.copyto(dest, src, casting='same_kind')

    def zeros(self, shape):
        return np.zeros(shape=shape, dtype=self.dtype)

    # ---------------- Mathematical Operations ---------------- #

    def transpose(self, a):
        # Returned a transposed view of a 2-D array
        return a.T

    def sum(self, a, axis, out):
        if len(out.shape) == 2:
            keepdims = True
        else:
            keepdims = False
        np.sum(a, axis=axis, dtype=self.dtype, out=out, keepdims=keepdims)

    @staticmethod
    def dot(a, b, out, transa='N', transb='N'):
        x = a.T if (transa == 'T') else a
        y = b.T if (transb == 'T') else b
        np.dot(x, y, out)

    @staticmethod
    def dot_add(a, b, out, transa='N', transb='N'):
        x = a.T if (transa == 'T') else a
        y = b.T if (transb == 'T') else b
        out[:] += np.dot(x, y)

    @staticmethod
    def elem_mult(a, b, out):
        np.multiply(a, b, out)

    @staticmethod
    def add_mm(a, b, out):
        assert a.shape == b.shape == out.shape
        out[:] = a + b

    @staticmethod
    def add_mv(a, b, out):
        assert len(a.shape) == 2
        assert len(b.shape) == 1
        out[:] = a + b

    # Activation functions

    @staticmethod
    def sigmoid(x, y):
        y[:] = 1. / (1. + np.exp(-x))

    @staticmethod
    def sigmoid_deriv(self, x, y, dy, dx):
        dx[:] = dy * y * (1. - y)

    @staticmethod
    def tanh(x, y):
        np.tanh(x, y)

    @staticmethod
    def tanh_deriv(x, y, dy, dx):
        dx[:] = dy * (1. - y * y)

    @staticmethod
    def rel(x, y):
        y[:] = x * (x > 0)

    @staticmethod
    def rel_deriv(x, y, dy, dx):
        dx[:] = dy * (x > 0)
