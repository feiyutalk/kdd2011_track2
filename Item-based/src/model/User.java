package model;

import java.util.ArrayList;
import java.util.Iterator;

public class User {
	private int id;
	private int ratingCount;
	private ArrayList<Rate> rates;
	
	public ArrayList<Rate> getRates() {
		return rates;
	}
	public void setRates(ArrayList<Rate> rates) {
		this.rates = rates;
	}
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public int getRatingCount() {
		return ratingCount;
	}
	public void setRatingCount(int ratingCount) {
		this.ratingCount = ratingCount;
	}
	
	@Override
	public String toString() {
		String info = "";
		info += (this.id + "|" + this.ratingCount +"\n");
		Iterator<Rate> iterator = this.rates.iterator();
		while(iterator.hasNext()){
			Rate rate = iterator.next();
			info += (rate.getItemId() + "\t" + rate.getScore() +"\n");
		}
		return info;
	}
	
	public boolean isRate(int songId){
		for(Rate rate : this.rates){
			if(rate.getItemId() == songId)
				return true;
		}
		return false;
	}
	
}
