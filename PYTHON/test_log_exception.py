import CLASSIFICATION.stif_nexterite_properties as stif

logger = stif.logger

try:
    raise Exception("Prout")
except Exception as e:
    logger.error(e,exc_info=True)
 
