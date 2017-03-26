package model;

public class Track {
	private int trackId;
	private int albumId;
	private int artistId;
	
	public Track(){
		
	}
	
	public Track(int trackId, int albumId, int artistId){
		this.trackId = trackId;
		this.albumId = albumId;
		this.artistId = artistId;
	}

	public int getTrackId() {
		return trackId;
	}

	public void setTrackId(int trackId) {
		this.trackId = trackId;
	}

	public int getAlbumId() {
		return albumId;
	}

	public void setAlbumId(int albumId) {
		this.albumId = albumId;
	}

	public int getArtistId() {
		return artistId;
	}

	public void setArtistId(int artistId) {
		this.artistId = artistId;
	}

	@Override
	public String toString() {
		String info = this.trackId + "|" + this.albumId + "|" + this.artistId;
		return info;
	}
	
}
