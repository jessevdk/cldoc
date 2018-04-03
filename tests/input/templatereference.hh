#include <string>
#include <list>

/**
 * Foo method.
 */
std::list<std::string> foo();

template <typename T>
struct WithInner {
    typedef T Type;
};

typedef std::list<WithInner<int>::Type> WithInnerIntType;
