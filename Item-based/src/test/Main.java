package test;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import recommender.ContentBasedRecommender;
import recommender.ItemBasedRecommender;

import model.Rate;
import model.Track;
import model.User;

import utils.Parse;

public class Main {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
//		File trainFile = new File("F:/tmp/lastData/newtrack5000.txt");
//		ArrayList<User> trainUsers = Parse.readUserAndRate(trainFile);
//		
//		File testFile = new File("F:/tmp/lastData/newtest5000.txt");
//		ArrayList<User> testUsers = Parse.readUserAndRate(testFile);
//		
//		for(User testUser : testUsers){
//			User testUserWithRecom = ItemBasedRecommender.getTestUserWithCFValue(testUser, trainUsers);
//			try {
//				Parse.writeFileWithOneUser(new File("F:/tmp/lastData/CFRecomm.txt"), testUserWithRecom);
//			} catch (IOException e) {
//				// TODO Auto-generated catch block
//				e.printStackTrace();
//			}
//		}
		
		File trainFile = new File("F:/tmp/lastData/deletegenre.txt");
		Hashtable<Integer, User> trainUsers = Parse.readUserAndRate(trainFile);
		
		File testFile = new File("F:/tmp/lastData/newtest5000.txt");
		Hashtable<Integer, User> testUsers = Parse.readUserAndRate(testFile);
		
		File file = new File("F:/tmp/lastData/newtrack5000.txt");
		Map<Integer, Track> tracks =  Parse.readTracks(file);
		
		Set<Map.Entry<Integer, User>> set = testUsers.entrySet();
		for(Entry<Integer, User> entry : set){
			User testUser = entry.getValue();
			User testUserWithRecom = ContentBasedRecommender.getTestUserWithCBValue(testUser, trainUsers,
					tracks);
			try {
				Parse.writeFileWithOneUser(new File("F:/tmp/data/CFRecomm.txt"), testUserWithRecom);
			} catch (IOException e) {
				e.printStackTrace();
			}
	}
	}

}
