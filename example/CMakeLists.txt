cmake_minimum_required(VERSION 2.6)
project(transport)

set(SOURCES transport/bicycle.cc transport/mountainbike.cc transport/racingbike.cc)
set(HEADERS transport/bicycle.hh transport/mountainbike.hh transport/racingbike.hh)

include_directories("${PROJECT_SOURCE_DIR}")
add_library(transport ${SOURCES})

find_program(CLDOC cldoc)

if(NOT DOCS_OUTPUT_DIR)
	set(DOCS_OUTPUT_DIR "gendocs" CACHE STRING "Generated documentation output directory" FORCE)
endif()

if(NOT DOCS_DIR)
	set(DOCS_DIR "" CACHE STRING "Location of external documentation files to be merged in" FORCE)
endif()

if(NOT ${CLDOC} STREQUAL "CLDOC-NOTFOUND")
  if(NOT ${DOCS_DIR} STREQUAL "")
  	set(CLDOC_MERGE "--merge ${DOCS_DIR}")
  else()
  	set(CLDOC_MERGE "")
  endif()

  add_custom_target(docs COMMAND
    ${CLDOC} generate
    ${CMAKE_CXX_FLAGS}
    -I${PROJECT_SOURCE_DIR}
    --
    ${CLDOC_MERGE}
    --output ${DOCS_OUTPUT_DIR}
    ${HEADERS}
    ${SOURCES}
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
  )

  set_target_properties(docs PROPERTIES
    EXCLUDE_FROM_ALL 1
    EXCLUDE_FROM_DEFAULT_BUILD 1
  )

  add_custom_target(serve_docs COMMAND
    ${CLDOC} serve -- ${DOCS_OUTPUT_DIR}
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
  )

  set_target_properties(docs PROPERTIES
    EXCLUDE_FROM_ALL 1
    EXCLUDE_FROM_DEFAULT_BUILD 1
  )

  add_dependencies(serve_docs docs)
else()
  message(STATUS
    "Documentation will not be generated"
  )
endif()
