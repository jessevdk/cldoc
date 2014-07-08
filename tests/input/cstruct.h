typedef struct
{
	int I;
	float F;
} A;

A    *a_new  (void);
void  a_free (A *a);

int   a_i (A *a);
float a_f (A *a);
