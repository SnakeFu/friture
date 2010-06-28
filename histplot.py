#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Timoth￩e Lecomte

# This file is part of Friture.
#
# Friture is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
#
# Friture is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Friture.  If not, see <http://www.gnu.org/licenses/>.

import classplot
import PyQt4.Qwt5 as Qwt
from PyQt4 import QtCore, Qt, QtGui
from numpy import zeros, ones, log10, linspace, logspace, interp, log2, histogram
from log2_scale_engine import QwtLog10ScaleEngine
import log2scale

# The peak decay rates (magic goes here :).
PEAK_DECAY_RATE = 1.0 - 3E-6
# Number of cycles the peak stays on hold before fall-off.
PEAK_FALLOFF_COUNT = 32 # default : 16

class FreqScaleDraw(Qwt.QwtScaleDraw):
	def __init__(self, *args):
		Qwt.QwtScaleDraw.__init__(self, *args)

	def label(self, value):
		#if value >= 1e3:
		#	label = "%gk" %(value/1e3)
		#else:
		label = "%d" %(value)
		return Qwt.QwtText(label)

class picker(Qwt.QwtPlotPicker):
	def __init__(self, *args):
		Qwt.QwtPlotPicker.__init__(self, *args)
		
	def trackerText(self, pos):
		pos2 = self.invTransform(pos)
		return Qwt.QwtText("%d Hz, %.1f dB" %(pos2.x(), pos2.y()))

	def drawTracker(self, painter):
		textRect = self.trackerRect(painter.font())
		if not textRect.isEmpty():
		  	   label = self.trackerText(self.trackerPosition())
		  	   if not label.isEmpty():
		  	   	   painter.save()
		  	   	   painter.setPen(Qt.Qt.NoPen)
		  	   	   painter.setBrush(Qt.Qt.white)
		  	   	   painter.drawRect(textRect)
		  	   	   painter.setPen(Qt.Qt.black)
		  	   	   #painter->setRenderHint(QPainter::TextAntialiasing, false);
		  	   	   label.draw(painter, textRect)
		  	   	   painter.restore()

class HistogramItem(Qwt.QwtPlotItem):

	Auto = 0
	Xfy = 1
	
	def __init__(self, *args):
		Qwt.QwtPlotItem.__init__(self, *args)
		self.__attributes = HistogramItem.Auto
		self.__data = Qwt.QwtIntervalData()
		self.__color = Qt.QColor()
		self.__reference = 0.0
		self.setItemAttribute(Qwt.QwtPlotItem.AutoScale, True)
		self.setItemAttribute(Qwt.QwtPlotItem.Legend, True)
		self.setZ(20.0)

	def setData(self, data):
		self.__data = data
		self.itemChanged()

	def data(self):
		return self.__data

	def setColor(self, color):
		if self.__color != color:
			self.__color = color
			self.itemChanged()

	def color(self):
		return self.__color

	def boundingRect(self):
		result = self.__data.boundingRect()
		if not result.isvalid():
			return result
		if self.testHistogramAttribute(HistogramItem.Xfy):
			result = Qwt.QwtDoubleRect(result.y(), result.x(),
									   result.height(), result.width())
			if result.left() > self.baseline():
				result.setLeft(self.baseline())
			elif result.right() < self.baseline():
				result.setRight(self.baseline())
		else:
			if result.bottom() < self.baseline():
				result.setBottom(self.baseline())
			elif result.top() > self.baseline():
				result.setTop(self.baseline())
		return result

	def rtti(self):
		return Qwt.QwtPlotItem.PlotHistogram

	def draw(self, painter, xMap, yMap, rect):
		iData = self.data()
		painter.setPen(self.color())
		x0 = xMap.transform(self.baseline())
		y0 = yMap.transform(self.baseline())
		for i in range(iData.size()):
			if self.testHistogramAttribute(HistogramItem.Xfy):
				x2 = xMap.transform(iData.value(i))
				if x2 == x0:
					continue

				y1 = yMap.transform(iData.interval(i).minValue())
				y2 = yMap.transform(iData.interval(i).maxValue())

				if y1 > y2:
					y1, y2 = y2, y1
					
				if  i < iData.size()-2:
					yy1 = yMap.transform(iData.interval(i+1).minValue())
					yy2 = yMap.transform(iData.interval(i+1).maxValue())

					if y2 == min(yy1, yy2):
						xx2 = xMap.transform(iData.interval(i+1).minValue())
						if xx2 != x0 and ((xx2 < x0 and x2 < x0)
										  or (xx2 > x0 and x2 > x0)):
							# One pixel distance between neighboured bars
							y2 += 1

				self.drawBar(
					painter, Qt.Qt.Horizontal, Qt.QRect(x0, y1, x2-x0, y2-y1))
			else:
				y2 = yMap.transform(iData.value(i))
				if y2 == y0:
					continue

				x1 = xMap.transform(iData.interval(i).minValue())
				x2 = xMap.transform(iData.interval(i).maxValue())

				if x1 > x2:
					x1, x2 = x2, x1

				if i < iData.size()-2:
					xx1 = xMap.transform(iData.interval(i+1).minValue())
					xx2 = xMap.transform(iData.interval(i+1).maxValue())
					x2 = min(xx1, xx2)
					yy2 = yMap.transform(iData.value(i+1))
					if x2 == min(xx1, xx2):
						if yy2 != 0 and (( yy2 < y0 and y2 < y0)
										 or (yy2 > y0 and y2 > y0)):
							# One pixel distance between neighboured bars
							x2 -= 1
				
				self.drawBar(
					painter, Qt.Qt.Vertical, Qt.QRect(x1, y0, x2-x1, y2-y0))

	def setBaseline(self, reference):
		if self.baseline() != reference:
			self.__reference = reference
			self.itemChanged()
	
	def baseline(self,):
		return self.__reference

	def setHistogramAttribute(self, attribute, on = True):
		if self.testHistogramAttribute(attribute):
			return

		if on:
			self.__attributes |= attribute
		else:
			self.__attributes &= ~attribute

		self.itemChanged()

	def testHistogramAttribute(self, attribute):
		return bool(self.__attributes & attribute) 

	def drawBar(self, painter, orientation, rect):
		painter.save()
		color = painter.pen().color()
		r = rect.normalized()
		factor = 125
		light = color.light(factor)
		dark = color.dark(factor)

		painter.setBrush(color)
		painter.setPen(Qt.Qt.NoPen)
		Qwt.QwtPainter.drawRect(painter, r.x()+1, r.y()+1,
								r.width()-2, r.height()-2)

		painter.setBrush(Qt.Qt.NoBrush)

		painter.setPen(Qt.QPen(light, 2))
		Qwt.QwtPainter.drawLine(
			painter, r.left()+1, r.top()+2, r.right()+1, r.top()+2)

		painter.setPen(Qt.QPen(dark, 2))
		Qwt.QwtPainter.drawLine(
			painter, r.left()+1, r.bottom(), r.right()+1, r.bottom())

		painter.setPen(Qt.QPen(light, 1))
		Qwt.QwtPainter.drawLine(
			painter, r.left(), r.top() + 1, r.left(), r.bottom())
		Qwt.QwtPainter.drawLine(
			painter, r.left()+1, r.top()+2, r.left()+1, r.bottom()-1)

		painter.setPen(Qt.QPen(dark, 1))
		Qwt.QwtPainter.drawLine(
			painter, r.right()+1, r.top()+1, r.right()+1, r.bottom())
		Qwt.QwtPainter.drawLine(
			painter, r.right(), r.top()+2, r.right(), r.bottom()-1)

		painter.restore()


class HistPlot(Qwt.QwtPlot):
	def __init__(self, parent, logger):
		Qwt.QwtPlot.__init__(self)

		# store the logger instance
		self.logger = logger

		# we do not need caching
		self.canvas().setPaintAttribute(Qwt.QwtPlotCanvas.PaintCached, False)
		self.canvas().setPaintAttribute(Qwt.QwtPlotCanvas.PaintPacked, False)

		self.setAxisScale(Qwt.QwtPlot.yLeft, -140., 0.)
		xtitle = Qwt.QwtText('Frequency (Hz)')
		xtitle.setFont(QtGui.QFont(8))
		self.setAxisTitle(Qwt.QwtPlot.xBottom, xtitle)
		# self.setAxisTitle(Qwt.QwtPlot.xBottom, 'Frequency (Hz)')
		ytitle = Qwt.QwtText('PSD (dB A)')
		ytitle.setFont(QtGui.QFont(8))
		self.setAxisTitle(Qwt.QwtPlot.yLeft, ytitle)
		# self.setAxisTitle(Qwt.QwtPlot.yLeft, 'PSD (dB)')

		# attach a grid
		grid = Qwt.QwtPlotGrid()
		grid.enableX(False)
		grid.setMajPen(Qt.QPen(Qt.QPen(Qt.Qt.gray)))
		grid.setMinPen(Qt.QPen(Qt.QPen(Qt.Qt.lightGray)))
		grid.attach(self)

		self.needfullreplot = False

		self.setAxisScale(Qwt.QwtPlot.xBottom, 85., 12000.)
		#self.setAxisScaleEngine(Qwt.QwtPlot.xBottom, )
		
		try:
			s = Qwt.QwtLog10ScaleEngine()
			s.autoscale(1,1.,1.)
		except:
			print "The loaded PyQwt library has buggy QwtScaleEngine (and friends) SIP declarations"
			print "... use a log10 scale engine instead of a log2 scale engine"
			self.setAxisScaleEngine(Qwt.QwtPlot.xBottom, Qwt.QwtLog10ScaleEngine())
		else:
			self.setAxisScaleEngine(Qwt.QwtPlot.xBottom, log2scale.CustomScaleEngine())
		
		self.setAxisScaleDraw(Qwt.QwtPlot.xBottom, FreqScaleDraw())
		
		self.paint_time = 0.

		# picker used to display coordinates when clicking on the canvas
		self.picker = picker(Qwt.QwtPlot.xBottom,
							   Qwt.QwtPlot.yLeft,
							   Qwt.QwtPicker.PointSelection,
							   Qwt.QwtPlotPicker.CrossRubberBand,
							   Qwt.QwtPicker.ActiveOnly,
							   self.canvas())
		
		# insert an additional curve for the peak
		#self.curve_peak = Qwt.QwtPlotCurve()
		#self.curve_peak.setPen(QtGui.QPen(Qt.Qt.blue))
		#self.curve_peak.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
		#self.curve_peak.attach(self)
		#self.peak = zeros((1,))
		#self.peakHold = 0
		#self.peakDecay = PEAK_DECAY_RATE
		
		self.histogram = HistogramItem()
		self.histogram.setColor(Qt.Qt.darkGreen)
		self.histogram.setBaseline(-200.)
		
		numValues = 20
		intervals = []
		values = Qwt.QwtArrayDouble(numValues)

		import random

		pos = 0.0
		for i in range(numValues):
			width = 5 + random.randint(0, 4)
			value = random.randint(0, 99)
			intervals.append(Qwt.QwtDoubleInterval(pos, pos+width))
			values[i] = value
			pos += width

		self.histogram.setData(Qwt.QwtIntervalData(intervals, values))
		self.histogram.attach(self)
		
		self.cached_canvas = self.canvas()
		
		# set the size policy to "Preferred" to allow the widget to be shrinked under the default size, which is quite big
		self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)

	def setdata(self, fl, fh, y):
		intervals = []
		values = Qwt.QwtArrayDouble(len(y))
		i = 0
		
		for flow, fhigh, value in zip(fl, fh, y):
			interval = Qwt.QwtDoubleInterval(flow, fhigh)
			intervals += [interval]
			values[i] = value
			i += 1
		
		self.histogram.setData(Qwt.QwtIntervalData(intervals, values))
		
		#self.compute_peaks(y_interp)
		#self.curve_peak.setData(self.xscaled, self.peak)
		
		if self.needfullreplot:
			self.needfullreplot = False
			self.replot()
		else:
			# self.replot() would call updateAxes() which is dead slow (probably because it
			# computes label sizes); instead, let's just ask Qt to repaint the canvas next time
			# This works because we disable the cache
			self.cached_canvas.update()

#		def compute_peaks(self, y):
#				if len(self.peak) <> len(y):
#			y_ones = ones(y.shape)
#			self.peak = y_ones*(-500.)
#			self.peakHold = zeros(y.shape)
#			self.dBdecay = y_ones * 20. * log10(PEAK_DECAY_RATE)
#
#		mask1 = (self.peak < y)
#		mask2 = (-mask1) * (self.peakHold > (PEAK_FALLOFF_COUNT - 1.))
#		mask2_a = mask2 * (self.peak + self.dBdecay < y)
#		mask2_b = mask2 * (self.peak + self.dBdecay >= y)
#
#		self.peak[mask1] = y[mask1]
#		self.peak[mask2_a] = y[mask2_a]
#		self.peak[mask2_b] = self.peak[mask2_b] + self.dBdecay[mask2_b]
#		
#		self.dBdecay[mask1] = 20. * log10(PEAK_DECAY_RATE)
#		self.dBdecay[mask2_b] = 2 * self.dBdecay[mask2_b]
#		
#		self.peakHold[mask1] = 0
#		self.peakHold += 1
	
	def setspecrange(self, min, max):
		self.setAxisScale(Qwt.QwtPlot.yLeft, min, max)
		self.needfullreplot = True
	
	def setweighting(self, weighting):
		if weighting is 0:
			title = "PSD (dB)"
		elif weighting is 1:
			title = "PSD (dB A)"
		elif weighting is 2:
			title = "PSD (dB B)"
		else:
			title = "PSD (dB C)"
		
		ytitle = Qwt.QwtText(title)
		ytitle.setFont(QtGui.QFont(8))
		self.setAxisTitle(Qwt.QwtPlot.yLeft, ytitle)
	
	def drawCanvas(self, painter):
		t = QtCore.QTime()
		t.start()
		Qwt.QwtPlot.drawCanvas(self, painter)
		self.paint_time = (95.*self.paint_time + 5.*t.elapsed())/100.
