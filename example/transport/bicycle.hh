#ifndef __TRANSPORT_BICYCLE_H__
#define __TRANSPORT_BICYCLE_H__

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

#endif /* __TRANSPORT_BICYCLE_H__ */
