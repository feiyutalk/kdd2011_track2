package utils;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import model.Rate;
import model.Track;
import model.User;

public class Parse {
	
	public static Map<Integer, Track> readTracks(File file){
		BufferedReader reader = null;
		Map<Integer,Track> tracks = null;
		try {
			tracks = new HashMap<Integer, Track>();
			reader = new BufferedReader(new FileReader(file));
			String trackLine = "";
			while((trackLine = reader.readLine()) != null){
				if(trackLine.contains("|")){
					Track track = formatTrack(trackLine);
					int trackId = track.getTrackId();
					tracks.put(trackId, track);
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}finally{
			try {
				reader.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		return tracks;
	}
	
	private static Track formatTrack(String trackLine) {
		Track track = new Track();
		String[] infos = trackLine.split("\\|");
		int trackId = 0;
		int albumId = 0;
		int artistId = 0;
		
		trackId = Integer.parseInt(infos[0]);
		if(infos.length >=2){
			if(!infos[1].equals("None"))
				albumId = Integer.parseInt(infos[1]);
		}
		if(infos.length >=3){
			if(!infos[2].equals("None"))
				artistId = Integer.parseInt(infos[2]);
		}
		track.setTrackId(trackId);
		track.setAlbumId(albumId);
		track.setArtistId(artistId);
		return track;
	}

	public static Hashtable<Integer, User> readUserAndRate(File file){
		BufferedReader reader = null;
		Hashtable<Integer, User> users = null;
		try {
			users = new Hashtable<Integer, User>();
			reader = new BufferedReader(new FileReader(file));
			String userLine = "";
			while((userLine = reader.readLine()) != null){
				if(userLine.contains("|")){
					User user = formatUser(userLine);
					ArrayList<Rate> rates = new ArrayList<Rate>();
					String rateLine = "";
					for(int i =0; i<user.getRatingCount(); i++){
						rateLine = reader.readLine();
						Rate rate = formatRate(rateLine);
						rates.add(rate);
					}
					user.setRates(rates);
					users.put(user.getId(), user);
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}finally{
			try {
				reader.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		return users;
	}
	
	private static User formatUser(String line){
		User user = new User();
		String[] infos = line.split("\\|");
		int id = Integer.parseInt(infos[0]);
		int count = Integer.parseInt(infos[1]);
		user.setId(id);
		user.setRatingCount(count);
		return user;
	}
	
	private static Rate formatRate(String line){
		Rate rate = new Rate();
		String[] infos = line.split("\t");
		int songId = Integer.parseInt(infos[0]);
		int score = Integer.parseInt(infos[1]);
		rate.setItemId(songId);
		rate.setScore(score);
		return rate;
	}
	
	public static void writeUserAndRate(File file, ArrayList<User> users) throws IOException{
		for(User user : users){
			Parse.writeFileWithOneUser(file, user);
		}
	}
	
	public static void writeFileWithOneUser(File file, User testUserWithCFValue) throws IOException{
		BufferedWriter writer = new BufferedWriter(new FileWriter(file, true));
		String head = testUserWithCFValue.getId() + "|" + testUserWithCFValue.getRatingCount();
		System.out.println(head);
		writer.write(head);
		writer.write("\r\n");
		ArrayList<Rate> rates = testUserWithCFValue.getRates();
		for(Rate rate : rates){
			System.out.println(rate.getItemId() + "\t" + rate.getScore());
			writer.write(rate.getItemId() + "\t" + rate.getScore());
			writer.write("\r\n");
		}
		writer.close();
	}
	
	public static void buildInvertedIndexTable(File file, Hashtable<Integer, User> users,
				HashMap<Integer, Track> tracks) throws IOException{
		BufferedWriter writer = new BufferedWriter(new FileWriter(file, true));
		
		Set<Map.Entry<Integer, Track>> trackEntries = tracks.entrySet();
		Iterator<Map.Entry<Integer, Track>> trackIterator = trackEntries.iterator();
		while(trackIterator.hasNext()){
			Track track = (Track) trackIterator.next();
			ArrayList<Integer> usersIdOfTrack = new ArrayList<Integer>();
			int numberOfUsers = 0;
			
			Set<Map.Entry<Integer, User>> userEntries = users.entrySet();
			Iterator<Map.Entry<Integer, User>> userInterator = userEntries.iterator();
			while(userInterator.hasNext()){
				User user = (User) userInterator.next();
				ArrayList<Rate> rates = user.getRates();
				for(int i =0; i<rates.size(); i++){
					if(rates.get(i).getItemId() == track.getTrackId()){
						numberOfUsers++;
						usersIdOfTrack.add(user.getId());
					}
				}
			}
			String head = track.getTrackId() + "|" + numberOfUsers;
			writer.write(head);
			writer.write("\r\n");
			for(Integer num : usersIdOfTrack){
				writer.write(num);
				writer.write("\r\n");
			}
		}
	}

}
