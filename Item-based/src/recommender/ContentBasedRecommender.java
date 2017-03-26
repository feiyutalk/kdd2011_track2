package recommender;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Hashtable;
import java.util.Map;

import model.Rate;
import model.Track;
import model.User;

public class ContentBasedRecommender {
	
	public static User getTestUserWithCBValue(User testUser, Hashtable<Integer, User> trainUsers,
			Map<Integer, Track> tracks){
		ArrayList<Rate> rates = testUser.getRates();
		User testUserWithCFValue = new User();
		testUserWithCFValue.setId(testUser.getId());
		testUserWithCFValue.setRatingCount(testUser.getRatingCount());
		
		ArrayList<Rate> ratesWithCBValue = new ArrayList<Rate>();
		for(int i = 0; i<rates.size(); i++){
			Rate testRate = rates.get(i);
			double cbValue = ContentBasedRecommender.getCBValue(testRate, testUser, trainUsers, tracks);
			Rate rateWithCBValue = new Rate(testRate.getItemId(), (int)(cbValue*10));
			ratesWithCBValue.add(rateWithCBValue);
		}
		Collections.sort(ratesWithCBValue);
		testUserWithCFValue.setRates(ratesWithCBValue);
		return testUserWithCFValue;
	}
	
	public static double getCBValue(Rate rate, User testUser , Hashtable<Integer, User> trainUsers, 
			 Map<Integer, Track> tracks){
		User trainUser = findTrainUser(trainUsers, testUser);
		if(trainUser == null)
			return 0;
		
		int trackId = rate.getItemId();
		int albumIdOfTheTrack  = findAlbumIdOfTrack(trackId, tracks);
		int artistIdOfTheTrack = findArtistIdOfTrack(trackId, tracks);

		int artistRate = getRate(artistIdOfTheTrack, trainUser);
		int albumRate = getRate(albumIdOfTheTrack, trainUser);
		
		double rateWithSameArtistId = getRateWithSameArtistId(trainUser, artistIdOfTheTrack, tracks);
		double rateWithSameAlbum = getRateWithSameAlbum(trainUser, albumIdOfTheTrack, tracks);
		
		double betaValue = getBetaValue(albumIdOfTheTrack, artistIdOfTheTrack);
		
		double rateScore = 1.0*(artistRate + albumRate) + rateWithSameArtistId + 
					 rateWithSameAlbum + betaValue;
		return rateScore;
	}
	
	public static double getRateWithSameArtistId(User trainUser, int artistId, Map<Integer, Track> tracks){
		if(artistId == 0)
			return 0;
		
		ArrayList<Rate> rates = trainUser.getRates();
		int count = 0;
		int allRate = 0;
		for(Rate rate : rates){
			int artistId2 = findArtistIdOfTrack(rate.getItemId(), tracks);
			if(artistId == artistId2){
				allRate += rate.getScore();
				count++;
			}
		}
		System.out.println("allRate:" + allRate+"|" + "count:"+count);
		return (count==0?0:(1.0*allRate/count));
	}
	
	public static double getRateWithSameAlbum(User trainUser, int albumId, Map<Integer, Track> tracks){
		if(albumId == 0)
			return 0;
		
		ArrayList<Rate> rates = trainUser.getRates();
		int count = 0;
		int allRate = 0;
		for(Rate rate : rates){
			int albumId2 = findAlbumIdOfTrack(rate.getItemId(), tracks);
			if(albumId == albumId2){
				allRate += rate.getScore();
				count++;
			}
		}
		System.out.println("allRate2:" + allRate + "|" + "count:" + count);
		return (count==0?0:(1.0*allRate/count));
	}
	
	public static User findTrainUser(Hashtable<Integer, User> users, User testUser){
		User user = users.get(testUser.getId());
		return user;
	}
	
	public static double getBetaValue(int albumId, int artistId){
		if(albumId == 0 && artistId == 0)
			return 35.0;
		else
			return 0.0;
	}
	
	public static boolean isSameArtist(int trackId1, int trackId2, Map<Integer, Track> tracks){
		int artistId1 = findArtistIdOfTrack(trackId1, tracks);
		int artistId2 = findArtistIdOfTrack(trackId2, tracks);
		return artistId1 == artistId2;
	}
	
	public static boolean isSameAlbum(int trackId1, int trackId2, Map<Integer, Track> tracks){
		int albumId1 = findAlbumIdOfTrack(trackId1, tracks);
		int albumId2 = findAlbumIdOfTrack(trackId2, tracks);
		return albumId1 == albumId2;
	}
	
	public static int getRate(int itemId, User user){
		ArrayList<Rate> rates = user.getRates();
		for(Rate rate : rates){
			if(rate.getItemId() == itemId){
				return rate.getScore();
			}
		}
		return 0;
	}
	
	public static int findAlbumIdOfTrack(int trackId, Map<Integer, Track> tracks){
		Track track = tracks.get(trackId);
		if(track != null){
			return track.getAlbumId();
		}
		return -1;
	}
	
	public static int findArtistIdOfTrack(int trackId, Map<Integer, Track> tracks){
		Track track = tracks.get(trackId);
		if(track != null){
			return track.getArtistId();
		}
		return -1;
	}
}
