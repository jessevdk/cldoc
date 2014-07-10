namespace N
{
	struct A
	{
		bool operator<(const A &other);
	};

	bool operator==(const A &a, const A &b);
}
