class Base
{
public:
	/* A b method.
	 *
	 * The b method description.
	 */
	virtual void b() = 0;
};

/*
 * The class A.
 *
 * A longer description of A.
 */
class A : public Base
{
public:
	/* @inherit */
	virtual void b() {}
};
