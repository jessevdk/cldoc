---
layout: page
---

# Documenting code
cldoc tries to make documenting your code as simple as possible. This page
describes the format for documenting various parts of your code.

# Writing comments
To associate documentation with a particular symbol, element or section of your
code, cldoc takes the same approach as other existing documentation tools. You
simply write a comment right above the symbol that you wish to document.

The format to document a symbol is simple. Lets start with a class.

## A class
{% highlight c++ %}
namespace transport
{
	/* Standard bicycle class.
	 *
	 * Bicycle implements a standard bicycle. Bicycles are a useful way of
	 * transporting oneself, without too much effort (unless you go uphill
	 * or against the wind). If there are a lot of people on the road, you
	 * can use <RingBell> to ring your bell (**note**, not all bicycles
	 * have bells!).
	 */
	class Bicycle
	{
	public:
		// PedalHarder makes you go faster (usually).
		virtual void PedalHarder();

		/* Ring bell on the bike.
		 *
		 * RingBell rings the bell on the bike. Note that not all
		 * bikes have bells. */
		virtual void RingBell();

		// Default destructor.
		virtual ~Bicycle();
	};
}
{% endhighlight %}

A documentation section begins with an ordinary comment (so not /** or ///), and
continues over the next lines. Multiple comments following eachother are automatically
concatenated together. Both multiline and single line comments can be used.

The actual comment consists of several parts. Documentation for all symbols
always has a `brief` section and a `body` section. The `brief` section consists
of the first line of the comment (and is not optional). The `body` section
**is** optional, and makes up the rest of the comment. There are two other
sections which are used for [functions and methods](#functions_and_methods)
(we'll come to that later).

The second thing to notice is that documentation is written in
[Markdown](http://daringfireball.net/projects/markdown). Here we used it to
make **note** strong. All of the markdown syntax is supported (cldoc uses
[showdown](https://github.com/coreyti/showdown) in the webapp).

The last thing that is noteworthy is the use of `<RingBell>` to create a cross-reference
to another symbol. When the documentation is extracted, all cross-references
are resolved from their current context (same as c++ itself does). So, we can
refer to `RingBell` from the `Bicycle` documentation, but from outside
`Bicycle` we need to use `Bicycle::RingBell`.

## A subclass
Lets extend our standard bicycle class with a racing bike.

{% highlight c++ %}
#include <transport/bicycle.hh>

namespace transport
{
	/* Racing bike class.
	 *
	 * RacingBike is a special kind of bike which can go much faster
	 * on the road, with much less effort (even uphill!). It doesn't make
	 * sense to call <RingBell> on a racing bike for they don't have bells.
	 */
	class RacingBike : public Bicycle
	{
	public:
		/* @inherit */
		virtual void PedalHarder();

		/* RingBell is not implemented. */
		virtual void RingBell();
	};
}
{% endhighlight %}

Here we see a new feature. When we implement the `RacingBike` subclass, we
subclass from `Bicycle`. Here we are going to reimplement `PedalHarder`, but
it doesn't really make sense to write another piece of documentation for
the function (it will still do the same, just differently implemented). Here
we can use the special `@inherit` comment which will copy the documentation
from the first base class which has a comment specified for the `PedalHarder`
method. This of course only works for `virtual` methods.

## Functions and Methods
We have seen most of the basic documentation comment syntax. There is still some
specific syntax left for documenting functions and methods.

{% highlight c++ %}
#include <transport/bicycle.hh>

namespace transport
{
	/* Mountain bike implementation of a <Bicycle>.
	 *
	 * MountainBike is an implementation of a <Bicycle>
	 * providing a bike for cycling on rough terrain. Mountain bikes
	 * are pretty cool because they have stuff like **Suspension** (and
	 * you can even adjust it using <SetSuspension>). If you're looking
	 * for a bike for use on the road, you might be better off using a
	 * <RacingBike> though.
	 */
	class MountainBike : public Bicycle
	{
	public:
		/* Set suspension stiffness.
		 * @stiffness the suspension stiffness.
		 *
		 * SetSuspension changes the stiffness of the suspension
		 * on the bike. The method will return false if the stiffness
		 * could not be adjusted.
		 *
		 * @return true if the suspension was adjusted successfully,
		 *         false otherwise.
		 */
		bool SetSuspension(double stiffness);
	};
}
{% endhighlight %}

Here we document the arguments and the return value of a method. The syntax,
again, is simple. You use @*name* to document an argument, directly after the
`brief` section. Following the last parameter is the `body`. For methods with
a return value, the `@return` documents the return value after the `body`
section.

## Grouping symbols in categories
Symbols can be grouped in categories to improve logical separation of different
parts of your code. Normally, with C++ this is not so much of a necessity since
code should already be segmented by namespaces and classes. However, for C API,
this is not the case. To move a particular symbol into a category, you can
use add the following `directives` around the symbols you want to move:

{% highlight c++ %}
    /* cldoc:begin-category(name) */

    // here are your symbols

    /* cldoc:end-category() */
{% endhighlight %}

The category name can be anything, as long as it doesn't collide with any symbol
names. Categories can be nested just as any other symbol by using the `::` separator.

Documentation for categories can be written using external documentation files,
which is explained in the next section.

## Writing external documentation
It's often useful to write documentation in separate, external files instead of
having to write everything in a C++ file. For example, namespaces often do not
have a logical location to write documentation. Another reason is that writing
large pieces of documentation as C++ comments is cumbersome.

cldoc supports writing external documentation as markdown files (files ending
on .md). These files are read from a directory specified with the `--merge`
option of cldoc (see [Generating site](generating.html) for more information).
Each .md file contains one or more special headers which refer to the particular
symbol that it's documenting:

	#<cldoc:symbol>

The `symbol` is the C++ identifier (for example `transport` to document the
`transport` namespace). A file can contain more than one section so you don't
have to write separate files for each symbol.

Externally documented symbols which cannot be resolved when generating the
documentation, will automatically create a category with the symbol as the name.
This is useful because it allows you to easily write additional documentation
(like a manual or tutorial) by just writing simple .md files.

## Wrapping it up
To wrap it up, please have a look at the example
[transport project](https://github.com/jessevdk/cldoc/example) and the
corresponding generated [documentation](transport.html).
