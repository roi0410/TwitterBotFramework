# coding=utf-8
import hashlib
import json
import re
from importlib import machinery

from TBFW.constant import *
from TBFW.exceptions import *

logger = logging.getLogger(__name__)

class Plugin:
	def __init__(self, pluginPath):
		self.code = None
		self.isLoaded = False
		self.attributeId = hashlib.sha256(pluginPath.encode()).hexdigest()
		self.attributeValid = None
		self.attributePath = pluginPath
		self.attributeSize = None
		self.attributeFileName = self.attributePath.split("/")[-1]
		self.attributeName = self.attributeFileName.replace(".py", "")
		self.attributeTarget = None
		self.attributeType = None
		self.attributePriority = None
		self.attributeAttachedStream = None
		self.attributeRatio = None
		self.attributeHour = None
		self.attributeMinute = None
		self.attributeMultipleHour = None
		self.attributeMultipleMinute = None
		self.attributeHours = []
		self.attributeMinutes = []

	def isValid(self):
		pluginFilePattern = re.compile("^.*\.py$")
		if pluginFilePattern.match(self.attributeFileName) and os.path.isfile(self.attributePath):
			self.attributeValid = True
			return True
		else:
			self.attributeValid = False
			return False

	def load(self):
		if self.isValid():
			try:
				self.attributeSize = os.path.getsize(self.attributePath)

				try:
					loader = machinery.SourceFileLoader(self.attributeName, self.attributePath)
					plugin = loader.load_module(self.attributeName)
				except Exception as error:
					logger.warning(messageErrorLoadingPlugin.format(self.attributeName, self.attributePath, error))
					raise InvalidPluginSyntaxError

				self.code = plugin

				if not hasattr(plugin, pluginAttributeTarget):
					raise NotFoundPluginTargetError
				if getattr(plugin, pluginAttributeTarget).lower() not in pluginTypes:
					raise InvalidPluginTargetError
				self.attributeTarget = getattr(plugin, pluginAttributeTarget)
				self.attributeType = self.attributeTarget.lower()

				if self.attributeType in [pluginReply, pluginTimeline, pluginEvent, pluginOther]:
					maxArgs = 1
				else:
					maxArgs = 0
				if plugin.do.__code__.co_argcount != maxArgs:
					raise TooManyArgmentsForPluginError

				self.attributePriority = getattr(plugin, pluginAttributePriority, defaultAttributePriority)
				if self.attributeType in [pluginReply, pluginTimeline, pluginEvent, pluginOther]:
					self.attributeAttachedStream = getattr(plugin, pluginAttributeAttachedStream, defaultAttributeAttachedStream)
				self.attributeRatio = getattr(plugin, pluginAttributeRatio, defaultAttributeRatio)
				if type(self.attributeRatio).__name__ != "int":
					raise InvalidPluginRatioError

				if self.attributeType == pluginRegular:
					hours = []
					minutes = []
					pluginHour = getattr(plugin, pluginAttributeHour, defaultAttributeHour)
					pluginMinute = getattr(plugin, pluginAttributeMinute, defaultAttributeMinute)
					pluginMultipleHour = getattr(plugin, pluginAttributeMultipleHour, defaultAttributeMultipleHour)
					pluginMultipleMinute = getattr(plugin, pluginAttributeMultipleMinute, defaultAttributeMultipleMinute)

					if pluginHour != defaultAttributeHour:
						if isinstance(pluginHour, list):
							hours.extend(pluginHour)
						elif isinstance(pluginHour, int):
							hours.append(pluginHour)
						else:
							raise InvalidPluginScheduleError

					if pluginMinute != defaultAttributeMinute:
						if isinstance(pluginMinute, list):
							minutes.extend(pluginMinute)
						elif isinstance(pluginMinute, int):
							minutes.append(pluginMinute)
						else:
							raise InvalidPluginScheduleError

					if pluginMultipleHour != defaultAttributeMultipleHour:
						if isinstance(pluginMultipleHour, int):
							hours.extend(
								[i * pluginMultipleHour for i in range(oneDayHours) if dayStartHour <= i * pluginMultipleHour < oneDayHours]
							)
						else:
							raise InvalidPluginScheduleError

					if pluginMultipleMinute != defaultAttributeMultipleMinute:
						if isinstance(pluginMultipleMinute, int):
							minutes.extend(
								[i * pluginMultipleMinute for i in range(oneHourMinutes) if dayStartHour <= i * pluginMultipleMinute < oneHourMinutes]
							)
						else:
							raise InvalidPluginScheduleError

					hours = sorted(list(set(hours)))
					minutes = sorted(list(set(minutes)))
					if not hours:
						hours = list(range(oneDayHours))
					if not minutes:
						minutes = list(range(oneHourMinutes))
					self.attributeHours = hours
					self.attributeMinutes = minutes

				self.isLoaded = True
				logger.info(messageSuccessLoadingPlugin.format(self.attributeName, self.attributePath))

			except:
				logger.exception(messageErrorLoadingPlugin.format(self.attributeName, self.attributePath))

class PluginManager:
	def __init__(self):
		self.plugins = {}
		self.__initializePlugins()

		self.attachedAccountId = []

	def __initializePlugins(self):
		self.plugins = {pluginType: [] for pluginType in pluginTypes}

	def __isNewPlugin(self, plugin):
		for pluginType, currentPlugins in self.plugins.items():
			for anotherPlugin in currentPlugins:
				if anotherPlugin.attributeId == plugin.attributeId:
					return False
		return True

	def deletePlugin(self, pluginPath):
		plugin = Plugin(pluginPath)

		for pluginType, currentPlugins in self.plugins.items():
			i = 0
			for anotherPlugin in currentPlugins:
				if anotherPlugin.attributeId == plugin.attributeId:
					del self.plugins[pluginType][i]
					break
				i += 1

	def addPlugin(self, pluginPath):
		plugin = Plugin(pluginPath)
		plugin.load()
		if not plugin.isLoaded:
			return
		if plugin.attributeAttachedStream not in self.attachedAccountId and isinstance(plugin.attributeAttachedStream, int):
			self.attachedAccountId.append(plugin.attributeAttachedStream)

		if self.__isNewPlugin(plugin):
			self.plugins[plugin.attributeType].append(plugin)
		else:
			for pluginType, currentPlugins in self.plugins.items():
				i = 0
				for anotherPlugin in currentPlugins:
					if anotherPlugin.attributeId == plugin.attributeId:
						self.plugins[pluginType][i] = plugin
						break
					i += 1

	def searchAllPlugins(self):
		self.__initializePlugins()

		for pluginFile in os.listdir(pluginsDir):
			pluginPath = pluginsDir + "/" + pluginFile
			self.addPlugin(pluginPath)

		self.sortPluginsOrder()
		self.dumpPluginsList()

	def sortPluginsOrder(self):
		for pluginType in pluginTypes:
			self.plugins[pluginType] = [
				plugin for plugin in sorted(self.plugins[pluginType], key=lambda x: x.attributePriority, reverse=True)
			]

	def getPluginsList(self):
		result = []
		for pluginType, currentPlugins in self.plugins.items():
			for plugin in currentPlugins:
				tmp = {
					"id": plugin.attributeId,
					"path": plugin.attributePath,
					"size": plugin.attributeSize,
					"type": plugin.attributeType,
					"isValid": plugin.attributeValid,
					"attachedStream": plugin.attributeAttachedStream,
					"ratio": plugin.attributeRatio,
					"name": plugin.attributeName
				}
				if pluginType == pluginRegular:
					tmp["hours"] = plugin.attributeHours
					tmp["minutes"] = plugin.attributeMinutes
				result.append(tmp)
		return result

	def dumpPluginsList(self):
		result = self.getPluginsList()
		path = apiDir + "/plugins.json"
		with open(path, "w") as f:
			json.dump(result, f, sort_keys=True, indent=4)
