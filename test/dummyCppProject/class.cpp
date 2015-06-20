#include "class.h"

using namespace NSXX::NSX;

template<typename T>
class F {
};

template<typename T>
class G {
};

class J {};
typedef J JJ;

class K {};

class H : public X, C, A, public G<int>{
  private:
    const NSXX::NSX::C *m;
    char c;
    F<int> d1;
    JJ j;
    K k[3];

  public:
    T x;
    void aPublicMethod() {}

  protected:
    int y;
    const NSXX::NSX::C *n;

    void aProtectedMethod();
};

namespace NSXX {
    namespace NSX {
        class E : public H {
        };
    }
}
