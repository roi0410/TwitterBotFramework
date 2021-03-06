# coding=utf-8
import os

currentDir = os.getcwd()
pathConfig = "config.json"
pathPluginsDir = "plugins"
pluginsDir = currentDir + "/" + pathPluginsDir
pathAssetsDir = "assets"
assetsDir = currentDir + "/" + pathAssetsDir
pathCacheDir = "cache"
cacheDir = currentDir + "/" + pathCacheDir
pathApiDir = "api"
apiDir = currentDir + "/" + pathApiDir
pathLogDir = "logs"
logDir = currentDir + "/" + pathLogDir
pathTmpDir = "tmp"
tmpDir = currentDir + "/" + pathTmpDir
dirs = [pluginsDir, logDir, apiDir, cacheDir, tmpDir, assetsDir]

pathThreadApi = "thread.json"

Reply = "REPLY"
Timeline = "TIMELINE"
DM = "DM"
Event = "EVENT"
Other = "OTHER"
Regular = "REGULAR"
Thread = "THREAD"
Initializer = "INITIALIZER"

pluginReply = "reply"
pluginTimeline = "timeline"
pluginDM = "dm"
pluginEvent = "event"
pluginThread = "thread"
pluginRegular = "regular"
pluginOther = "other"
pluginInitializer = "initializer"

pluginTypes = [
	pluginReply,
	pluginTimeline,
	pluginDM,
	pluginEvent,
	pluginThread,
	pluginRegular,
	pluginOther,
	pluginInitializer
]

messageLogFormat = "[%(asctime)s][%(threadName)s %(name)s/%(levelname)s]: %(message)s"
messageLogTimeFormat = "%H:%M:%S"
messageLogDatetimeFormat = "%Y-%m-%d_%H-%M-%S"
messageSuccessInitialization = "Initialization Complate. Current time is {0}."
messageErrorLoadingPlugin = "Plugin \"{0}\"({1}) could not be loaded. Error Detail:\n{2}"
messageSuccessLoadingPlugin = "Plugin \"{0}\"({1}) has been loaded successfully."
messageSuccessExecutingRegularPlugin = "Regular plugin \"{0}\" was executed successfully."
messageErrorExecutingRegularPlugin = "Regular plugin \"{0}\" could not be executed. Error Detail:\n{1}"
messageSuccessConnectingUserStream = "TBFW started @{0}'s streaming."
messageErrorConnectingUserStream = "Error occured while connecting to @{0}'s stream. TBFW will reconnect after {1} seconds."
messageErrorProcessingStream = "Error occured while processing @{0}'s stream."
messageErrorExecutingPlugin = "Error occured while executing plugin \"{0}\"."
messageTweetErrorExecutingPlugin = "@{0} Error occured while executing plugin \"{1}\". Please retry in minutes.\n\n詳細: {2}"
messageErrorConnectingTwitter = "Error occured while connecting to Twitter with HTTP Status Code {0}."

reconnectUserStreamSeconds = 10

pluginAttributeTarget = "TARGET"
pluginAttributePriority = "PRIORITY"
pluginAttributeAttachedStream = "ACCOUNT"
pluginAttributeRatio = "RATIO"
pluginAttributeHour = "HOUR"
pluginAttributeMultipleHour = "MULTIPLE_HOUR"
pluginAttributeMinute = "MINUTE"
pluginAttributeMultipleMinute = "MULTIPLE_MINUTE"

defaultAttributeValid = None
defaultAttributePath = None
defaultAttributeSize = None
defaultAttributeName = None
defaultAttributeTarget = None
defaultAttributePriority = 0
defaultAttributeAttachedStream = 0
defaultAttributeRatio = 1
defaultAttributeHour = None
defaultAttributeMultipleHour = None
defaultAttributeMinute = None
defaultAttributeMultipleMinute = None

dayStartHour = 0
oneHourMinutes = 60
oneDayHours = 24
