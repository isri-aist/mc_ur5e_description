if(NOT DEFINED INPUT_FILE)
  message(FATAL_ERROR "INPUT_FILE is required")
endif()

if(NOT DEFINED UR_DESCRIPTION_PREFIX)
  message(FATAL_ERROR "UR_DESCRIPTION_PREFIX is required")
endif()

file(READ "${INPUT_FILE}" URDF_CONTENT)

string(REPLACE "package://ur_description/" "file://${UR_DESCRIPTION_PREFIX}/"
               URDF_CONTENT "${URDF_CONTENT}")

file(WRITE "${INPUT_FILE}" "${URDF_CONTENT}")
