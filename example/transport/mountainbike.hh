#ifndef __TRANSPORT_MOUNTAIN_BIKE_H__
#define __TRANSPORT_MOUNTAIN_BIKE_H__

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

		/* Change the break type.
		 * @BreakType the break type.
		 * @breakType the type of the break.
		 *
		 * ChangesBreak changes the type of break fitted to the bike.
		 * The method will return false if the break type could not be
		 * fitted.
		 *
		 * @return true if the break was adjusted successfully.
		 *         false otherise
		 */
		template <typename BreakType>
		bool ChangeBreak(BreakType breakType)
		{
			if (breakType)
			{
				return true;
			}

			return false;
		}
	};
}

#endif /* __TRANSPORT_MOUNTAIN_BIKE_H__ */

