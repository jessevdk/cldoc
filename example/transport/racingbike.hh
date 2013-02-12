#ifndef __TRANSPORT_RACING_BIKE_H__
#define __TRANSPORT_RACING_BIKE_H__

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

#endif /* __TRANSPORT_RACING_BIKE_H__ */
