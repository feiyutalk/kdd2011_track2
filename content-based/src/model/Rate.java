package model;

public class Rate implements Comparable<Rate>{
	private int itemId;
	private int score;


	public int getItemId() {
		return itemId;
	}
	public void setItemId(int itemId) {
		this.itemId = itemId;
	}
	public int getScore() {
		return score;
	}
	public void setScore(int score) {
		this.score = score;
	}
	
	public Rate(){
		
	}
	
	public Rate(int songId, int score){
		this.itemId = songId;
		this.score = score;
	}
	
	@Override
	public int compareTo(Rate o) {
		// TODO Auto-generated method stub
		if(this.getScore() > o.getScore())
			return 1;
		else if(this.getScore() == o.getScore())
			return 0;
		else 
			return -1;
	}
	
}
