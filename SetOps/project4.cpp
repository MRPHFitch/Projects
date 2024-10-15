#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <algorithm>
#include <set>
using namespace std;

class SetOps{
public:
    SetOps();
    void display();
    void output(set<int> gimli);
    set<int> performOperations(const string& key1, const string& key2, char command, map<string, set<int>> info);
    set<int> addTogether(set<int> first, set<int> second);
    set<int> intersect(set<int> first, set<int> second);
    void readFile(map<string, set<int>> info);
};
//Create the map to use.
SetOps::SetOps(){
    map<string, set<int>> info;
}
//Create the union set
set<int> SetOps::addTogether(set<int> first, set<int> second){
    //Create the set to store the new resulting unionized set, then use algorithm method of union.
    set<int> result;
    set_union(first.cbegin(), first.cend(), second.cbegin(), second.cend(), inserter(result, result.begin()));
    return result;
}
set<int> SetOps::intersect(set<int> first, set<int> second){
    //Create the set to store the new resulting intersection of sets, and use the algorithm method of intersection.
    set<int> result;
    set_intersection(first.begin(), first.end(), second.begin(), second.end(),inserter(result, result.begin()));
    return result;
}
//Create a display method for the specific sets after they gone through set operations.
void SetOps::output(set<int> gimli){
    for(int num: gimli){
        cout<<num<<" ";
    }
    cout<<endl;
}
//Use a helper method to go through the specific set operations needed to be performed.
void SetOps::readFile(map<string, set<int>> info){
    //Establish the variables needed to determine which sets to compare and how to compare them.
    int numCompared=0;
    string key1, key2, key3, key4;
    char command, command2, command3;
    set<int> result, first, second;
    //Loop through the file until there are no more set operations left to perform.
    while(cin>>numCompared){
        //Find the first set for the comparison.
        cin>>key1;
        //Copy the set of IDs of the given key from the map into the set.
        first=info[key1];
        //Set the resulting output IDs to the given key's ID set before the loop.
        result=first;
        //Print out the number of sets to be compared and the key of the first set to ensure correct output.
        cout<<numCompared<<" "<<key1;
        //Loop through each set operation getting all the sets desired for set operations.
        for (int i = 0; i < numCompared-1; i++){
            //After getting the set operation command and the next set to be operated on, print them out so you get all
            //sets operated on printed out instead of just first and last.
            cin>>command;
            cin>>key2;
            cout<<" "<<command<<" "<<key2;
            //Use the second key two find the set in the map and copy it to a new set to preserve contents.
            second=info[key2];
            //Determine which method to call depending on which command has been given.
            switch (command){
            //Denotes OR case which means to do the union of the two sets.
            case 'O':
                //Store the resulting IDs. Use itself to call the method so that if there are multiple loops, it adjusts
                //each time. This way if you have a union of two sets, then intersect the result with another,
                //Everything is still maintained throughout the operations and loops. 
                result = addTogether(result, second);
                break;
            // Denotes AND which means the intersection of the two sets.
            case 'A':
                //Same thing as for the union call.
                result = intersect(result, second);
                break;
            }
        }
        //Print out the resulting list of ID's after all Set Operations have been completed.
        cout<<": ";
        output(result);
    }
}
int main(){
    //Establish necessary variables
    SetOps frodo;
    int lines, numContained, num;
    string title;
    //Read in the number of lines containing Set data.
    cin>>lines;
    int count=0;
    map<string, set<int>> info;
    //Loop through the document until you have read all Sets.
    while(count<lines){
        cin>>title>>numContained;
        set<int> ids;
        //After reading in the title for the sets, loop through all the IDs to establish the set values.
        for(int i=0; i<numContained; i++){
            cin>>num;
            ids.insert(num);
        }
        //After the set has been established, add the title and the set to the map. And increment the counter
        //To ensure you do not endless loop.
        info.insert(make_pair(title, ids));
        count++;
    }
    //Call the method to perform all the set operations then print out the map.
    frodo.readFile(info);
    cout<<endl;
    cout<<"Printing file data: "<<endl;
    for(const auto& entry: info){
        cout<<entry.first<<": ";
        frodo.output(entry.second);
    }
    return 0;
}