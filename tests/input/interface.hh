/*
 * The class A.
 *
 * A longer description of A.
 */
class A
{
public:
	/* An abstract a.
	 *
	 * A longer description of abstract a.
	 */
	virtual void a() = 0;
};

/*
 * The Impl class.
 *
 * The implementation class.
 */
class Impl : public A
{
public:
	// @inherit
	virtual void a() {}
};
