package recommender;
/**
 * 基于Item的协同过滤算法的推荐系统
 * 采用的相似度比较式最简单的那种
 */

import java.util.ArrayList;
import java.util.Collections;
import java.util.Hashtable;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import model.Rate;
import model.User;

public class ItemBasedRecommender {
	
	public static double getSimility(Rate rate1, Rate rate2, Hashtable<Integer, User> trainUsers){
		int count1 = 0, count2 =0, all = 0;
		if(rate1.getItemId() == rate2.getItemId())
			return 1;
		
		Set<Map.Entry<Integer, User>> entries = trainUsers.entrySet();
		for(Entry<Integer, User> entry : entries){
			User user = entry.getValue();
			if(user.isRate(rate1.getItemId())&&
					user.isRate(rate2.getItemId())){
				all++;
				count1++;
				count2++;
			}else if(user.isRate(rate1.getItemId())&&
						!user.isRate(rate2.getItemId())){
				count1++;
			}else if(!user.isRate(rate1.getItemId())&&
						user.isRate(rate2.getItemId())){
				count2++;
			}	
		}
		return (Math.max(count1, count2)==0? 0 : 1.0*all/Math.max(count1, count2)); 
	}
	
	public static ArrayList<Double> getSimilities(User trainUser, Rate testRate, 
			Hashtable<Integer, User> trainUsers){
		ArrayList<Double> similities = new ArrayList<Double>();
		ArrayList<Rate> rates = trainUser.getRates(); 
		for(int i=0; i<rates.size(); i++){
			Rate rate = rates.get(i);
			double simility = ItemBasedRecommender.getSimility(rate, testRate, trainUsers);
			similities.add(simility);
		}
		return similities;
	}
	
	public static double getCFValue(User testUser, Rate testRate, 
			Hashtable<Integer, User> trainUsers){
		User trainUser = ItemBasedRecommender.findTrainUser(trainUsers, testUser);
		if(trainUser == null)
			return 0;
		ArrayList<Double> similities = ItemBasedRecommender.getSimilities(trainUser, testRate, trainUsers);
		ArrayList<Rate> rates = trainUser.getRates();
		for(Rate rate : rates){
			if(rate.getItemId() == testRate.getItemId())
				return rate.getScore();
		}
		
		double cfValue = 0;
		for(int i=0; i<similities.size(); i++){
			Rate rate = rates.get(i);
			double simility = similities.get(i);
			cfValue += (rate.getScore()*simility);
		}
		return cfValue*10/rates.size();
	}
	
	public static User findTrainUser(Hashtable<Integer, User> users, User testUser){
		User user = users.get(testUser.getId());
		return user;
	}
	
	public static User getTestUserWithCFValue(User testUser, Hashtable<Integer, User> trainUsers){
		ArrayList<Rate> rates = testUser.getRates();
		User testUserWithCFValue = new User();
		testUserWithCFValue.setId(testUser.getId());
		testUserWithCFValue.setRatingCount(testUser.getRatingCount());
		
		ArrayList<Rate> ratesWithCFValue = new ArrayList<Rate>();
		for(int i=0; i<rates.size(); i++){
			Rate testRate = rates.get(i);
			double cfValue = ItemBasedRecommender.getCFValue(testUser, testRate, trainUsers);
			Rate rateWithCFValue = new Rate(testRate.getItemId(), (int)cfValue);
			ratesWithCFValue.add(rateWithCFValue);
		}
		Collections.sort(ratesWithCFValue);
		testUserWithCFValue.setRates(ratesWithCFValue);
		return testUserWithCFValue;
	}
}	
