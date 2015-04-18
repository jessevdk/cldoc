SOURCES = $(wildcard transport/*.cc)
HEADERS = $(wildcard transport/*.hh)

OBJECTS = ${SOURCES:.cc=.o}
CXXFLAGS = -I. -fPIC
TARGET = libtransport.so

COMMON_DOC_FLAGS = --report --merge docs --output html $(SOURCES) $(HEADERS)

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) -o $@ -shared $^

clean:
	@rm -f $(TARGET) $(OBJECTS)

doc:
	@echo "Generating documentation..."; \
	cldoc generate $(CXXFLAGS) -- $(COMMON_DOC_FLAGS)

static-doc:
	@echo "Generating static documentation..."; \
	cldoc generate $(CXXFLAGS) -- --static $(COMMON_DOC_FLAGS)

serve:
	cldoc serve html
