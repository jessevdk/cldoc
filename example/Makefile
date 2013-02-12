SOURCES = $(wildcard transport/*.cc)
HEADERS = $(wildcard transport/*.hh)

OBJECTS = ${SOURCES:.cc=.o}
CXXFLAGS = -I. -fPIC
TARGET = libtransport.so

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) -o $@ -shared $^

clean:
	@rm -f $(TARGET) $(OBJECTS)

doc:
	@echo "Generating documentation..."; \
	cldoc $(CXXFLAGS) -- 		\
		--report 		\
		--merge docs 		\
		--output html 		\
		$(SOURCES) $(HEADERS)

serve:
	cldoc -- --output html --serve
